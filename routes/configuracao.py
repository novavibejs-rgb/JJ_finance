from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from werkzeug.utils import secure_filename

from services.verificador_config import verificar_smtp
from services.email import enviar_email

from banco import configuracao

from utils.auth import somente_admin

import os


# =========================================================
# EXTENSÕES PERMITIDAS PARA LOGO
# =========================================================

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}


def extensao_permitida(nome_arquivo):
    return (
        "." in nome_arquivo
        and nome_arquivo.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# =========================================================
# BLUEPRINT
# =========================================================

configuracoes_bp = Blueprint(
    "configuracoes",
    __name__,
    url_prefix="/configuracoes"
)


# =========================================================
# CONFIGURAÇÕES
# SOMENTE ADMIN
# =========================================================

@configuracoes_bp.route(
    "/",
    methods=["GET", "POST"]
)
@somente_admin
def index():

    # =====================================================
    # BUSCAR CONFIGURAÇÕES
    # =====================================================

    config = configuracao.buscar_configuracao()

    email_config = (
        configuracao.buscar_configuracao_email()
    )


    # =====================================================
    # PROCESSAR POST
    # =====================================================

    if request.method == "POST":

        tipo_configuracao = request.form.get(
            "tipo_configuracao"
        )


        # =================================================
        # TESTAR SMTP
        # =================================================

        if tipo_configuracao == "testar_email":

            sucesso, mensagem = verificar_smtp()

            return render_template(
                "configuracoes/index.html",
                configuracao=config,
                email_config=email_config,
                mensagem_smtp=mensagem,
                sucesso_smtp=sucesso,
                configuracao_ativa="email"
            )


        # =================================================
        # ENVIAR E-MAIL DE TESTE
        # =================================================

        if tipo_configuracao == "enviar_email_teste":

            email_config = (
                configuracao.buscar_configuracao_email()
            )

            if not email_config:

                return render_template(
                    "configuracoes/index.html",
                    configuracao=config,
                    email_config=None,
                    mensagem_smtp=(
                        "Nenhuma configuração de "
                        "e-mail cadastrada."
                    ),
                    sucesso_smtp=False,
                    configuracao_ativa="email"
                )


            sucesso, mensagem = enviar_email(
                email_config["email"],
                "Teste - J&J Finance",
                "Este é um teste em texto do J&J Finance.",
                template_html="emails/teste.html"
            )


            return render_template(
                "configuracoes/index.html",
                configuracao=config,
                email_config=email_config,
                mensagem_smtp=mensagem,
                sucesso_smtp=sucesso,
                configuracao_ativa="email"
            )


        # =================================================
        # CONFIGURAÇÃO DA EMPRESA
        # =================================================

        if tipo_configuracao == "empresa":

            nome_empresa = request.form[
                "nome_empresa"
            ]

            telefone = request.form.get(
                "telefone"
            )

            email = request.form.get(
                "email"
            )

            endereco = request.form.get(
                "endereco"
            )

            logo = request.files.get(
                "logo"
            )


            # =============================================
            # UPLOAD DA LOGO
            # =============================================

            if logo and logo.filename:

                if not extensao_permitida(
                    logo.filename
                ):
                    return (
                        "Formato de imagem não permitido.",
                        400
                    )


                nome_arquivo = secure_filename(
                    logo.filename
                )


                pasta_logo = os.path.join(
                    "static",
                    "uploads",
                    "logos"
                )


                os.makedirs(
                    pasta_logo,
                    exist_ok=True
                )


                caminho_logo = os.path.join(
                    pasta_logo,
                    nome_arquivo
                )


                logo.save(
                    caminho_logo
                )


                logo = os.path.join(
                    "uploads",
                    "logos",
                    nome_arquivo
                )

            else:

                logo = config["logo"]


            # =============================================
            # SALVAR CONFIGURAÇÃO
            # =============================================

            configuracao.atualizar_configuracao(
                config["id"],
                nome_empresa,
                telefone,
                email,
                endereco,
                logo
            )


        # =================================================
        # CONFIGURAÇÃO DE E-MAIL
        # =================================================

        elif tipo_configuracao == "email":

            smtp_server = request.form[
                "smtp_server"
            ]

            smtp_port = request.form[
                "smtp_port"
            ]

            email = request.form[
                "email"
            ]

            senha = request.form[
                "senha"
            ]


            configuracao.salvar_ou_atualizar_configuracao_email(
                smtp_server,
                smtp_port,
                email,
                senha
            )


        # =================================================
        # REDIRECIONAMENTO
        # =================================================

        return redirect(
            url_for(
                "configuracoes.index"
            )
        )


    # =====================================================
    # CARREGAMENTO DA PÁGINA
    # =====================================================

    return render_template(
        "configuracoes/index.html",
        configuracao=config,
        email_config=email_config,
        configuracao_ativa="empresa"
    )

