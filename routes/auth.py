from datetime import datetime, timedelta
import secrets

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from banco.conexao import conectar
from services.email import enviar_email

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# =========================================================
# GERAR CÓDIGO DE 6 DÍGITOS
# =========================================================
def gerar_codigo():
    return f"{secrets.randbelow(1_000_000):06d}"


# =========================================================
# LOGIN
# =========================================================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("usuario_id"):
        return redirect(url_for("dashboard.index"))

    erro = None

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "")

        if not usuario or not senha:
            erro = "Preencha o usuário e a senha."
        else:
            conn = conectar()
            usuario_db = conn.execute(
                """
                SELECT *
                FROM usuarios
                WHERE usuario = ?
                  AND ativo = 1
                LIMIT 1
                """,
                (usuario,),
            ).fetchone()
            conn.close()

            if usuario_db and check_password_hash(usuario_db["senha"], senha):
                session.clear()
                session["usuario_id"] = usuario_db["id"]
                session["usuario_nome"] = usuario_db["nome"]
                session["usuario"] = usuario_db["usuario"]
                session["nivel"] = usuario_db["nivel"]

                return redirect(url_for("dashboard.index"))

            erro = "Usuário ou senha incorretos."

    return render_template("auth/login.html", erro=erro)


# =========================================================
# LOGOUT
# =========================================================
@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


# =========================================================
# RECUPERAÇÃO DE SENHA
# =========================================================
@auth_bp.route("/esqueci-senha", methods=["GET", "POST"])
def esqueci_senha():
    # =====================================================
    # PRIMEIRA ABERTURA
    # =====================================================
    if request.method == "GET":
        return render_template("auth/esqueci_senha.html", etapa="email")

    # =====================================================
    # DESCOBRIR QUAL ETAPA FOI ENVIADA
    # =====================================================
    etapa = request.form.get("etapa", "email")

    # =====================================================
    # ETAPA 1 — E-MAIL
    # =====================================================
    if etapa == "email":
        email = request.form.get("email", "").strip().lower()

        if not email:
            return render_template(
                "auth/esqueci_senha.html",
                etapa="email",
                erro="Preencha o e-mail.",
            )

        conn = conectar()

        usuario_db = conn.execute(
            """
            SELECT id, email
            FROM usuarios
            WHERE email = ?
              AND ativo = 1
            LIMIT 1
            """,
            (email,),
        ).fetchone()

        # =================================================
        # SE O USUÁRIO EXISTIR
        # =================================================
        if usuario_db:
            codigo = gerar_codigo()
            codigo_hash = generate_password_hash(codigo)
            expiracao = datetime.now() + timedelta(minutes=10)

            # ---------------------------------------------
            # INVALIDAR CÓDIGOS ANTERIORES
            # ---------------------------------------------
            conn.execute(
                """
                UPDATE recuperacao_senha
                SET usado = 1
                WHERE usuario_id = ?
                  AND usado = 0
                """,
                (usuario_db["id"],),
            )

            # ---------------------------------------------
            # SALVAR NOVO CÓDIGO
            # ---------------------------------------------
            conn.execute(
                """
                INSERT INTO recuperacao_senha (
                    usuario_id,
                    codigo_hash,
                    expiracao,
                    tentativas,
                    usado
                )
                VALUES (?, ?, ?, 0, 0)
                """,
                (usuario_db["id"], codigo_hash, expiracao),
            )

            conn.commit()
            conn.close()

            # =================================================
            # E-MAIL
            # =================================================
            mensagem = f"""Olá!

Recebemos uma solicitação para recuperar
a senha da sua conta no J&J Finance.

Seu código de recuperação é:

{codigo}

Este código é válido por 10 minutos.

Se você não solicitou a recuperação da senha,
ignore este e-mail.

Atenciosamente,

J&J Finance"""

            enviado, resposta = enviar_email(
                destinatario=email,
                assunto="Código de recuperação de senha - J&J Finance",
                mensagem=mensagem,
            )

            if not enviado:
                print("[ERRO RECUPERAÇÃO]", resposta)
        else:
            conn.close()

        # =================================================
        # NÃO REVELAR SE O E-MAIL EXISTE
        # =================================================
        sucesso = (
            "Se o e-mail estiver cadastrado, "
            "um código de recuperação será enviado."
        )

        return render_template(
            "auth/esqueci_senha.html",
            etapa="codigo",
            sucesso=sucesso,
            email=email,
        )

    # =====================================================
    # ETAPA 2 — VERIFICAR CÓDIGO
    # =====================================================
    if etapa == "codigo":
        email = request.form.get("email", "").strip().lower()
        codigo = request.form.get("codigo", "").strip()

        # =================================================
        # VALIDAÇÃO BÁSICA
        # =================================================
        if not email or not codigo:
            return render_template(
                "auth/esqueci_senha.html",
                etapa="codigo",
                email=email,
                erro="Digite o código recebido.",
            )

        if not codigo.isdigit() or len(codigo) != 6:
            return render_template(
                "auth/esqueci_senha.html",
                etapa="codigo",
                email=email,
                erro="O código deve possuir 6 dígitos.",
            )

        conn = conectar()

        # =================================================
        # BUSCAR USUÁRIO
        # =================================================
        usuario_db = conn.execute(
            """
            SELECT id
            FROM usuarios
            WHERE email = ?
              AND ativo = 1
            LIMIT 1
            """,
            (email,),
        ).fetchone()

        if not usuario_db:
            conn.close()
            return render_template(
                "auth/esqueci_senha.html",
                etapa="codigo",
                email=email,
                erro="Código inválido ou expirado.",
            )

        # =================================================
        # BUSCAR CÓDIGO MAIS RECENTE
        # =================================================
        recuperacao = conn.execute(
            """
            SELECT *
            FROM recuperacao_senha
            WHERE usuario_id = ?
              AND usado = 0
            ORDER BY id DESC
            LIMIT 1
            """,
            (usuario_db["id"],),
        ).fetchone()

        if not recuperacao:
            conn.close()
            return render_template(
                "auth/esqueci_senha.html",
                etapa="codigo",
                email=email,
                erro="Código inválido ou expirado.",
            )

        # =================================================
        # VERIFICAR EXPIRAÇÃO
        # =================================================
        expiracao = datetime.fromisoformat(str(recuperacao["expiracao"]))

        if datetime.now() > expiracao:
            conn.execute(
                """
                UPDATE recuperacao_senha
                SET usado = 1
                WHERE id = ?
                """,
                (recuperacao["id"],),
            )
            conn.commit()
            conn.close()

            return render_template(
                "auth/esqueci_senha.html",
                etapa="codigo",
                email=email,
                erro="O código expirou. Solicite um novo código.",
            )

        # =================================================
        # LIMITE DE TENTATIVAS
        # =================================================
        if recuperacao["tentativas"] >= 5:
            conn.close()
            return render_template(
                "auth/esqueci_senha.html",
                etapa="codigo",
                email=email,
                erro="Número máximo de tentativas atingido.",
            )

        # =================================================
        # VERIFICAR HASH DO CÓDIGO
        # =================================================
        codigo_correto = check_password_hash(
            recuperacao["codigo_hash"], codigo
        )

        if not codigo_correto:
            conn.execute(
                """
                UPDATE recuperacao_senha
                SET tentativas = tentativas + 1
                WHERE id = ?
                """,
                (recuperacao["id"],),
            )
            conn.commit()
            conn.close()

            return render_template(
                "auth/esqueci_senha.html",
                etapa="codigo",
                email=email,
                erro="Código inválido ou expirado.",
            )

        # =================================================
        # CÓDIGO CORRETO
        # =================================================
        conn.close()

        session["recuperacao_usuario_id"] = usuario_db["id"]
        session["recuperacao_codigo_id"] = recuperacao["id"]

        return render_template("auth/esqueci_senha.html", etapa="nova_senha")

    # =====================================================
    # ETAPA 3 — NOVA SENHA
    # =====================================================
    if etapa == "nova_senha":
        usuario_id = session.get("recuperacao_usuario_id")
        codigo_id = session.get("recuperacao_codigo_id")

        # =================================================
        # VERIFICAR SESSÃO DE RECUPERAÇÃO
        # =================================================
        if not usuario_id or not codigo_id:
            return redirect(url_for("auth.esqueci_senha"))

        nova_senha = request.form.get("nova_senha", "")
        confirmar_senha = request.form.get("confirmar_senha", "")

        # =================================================
        # VALIDAR SENHA
        # =================================================
        if len(nova_senha) < 8:
            return render_template(
                "auth/esqueci_senha.html",
                etapa="nova_senha",
                erro="A senha deve ter no mínimo 8 caracteres.",
            )

        if nova_senha != confirmar_senha:
            return render_template(
                "auth/esqueci_senha.html",
                etapa="nova_senha",
                erro="As senhas não são iguais.",
            )

        # =================================================
        # REGRAS DE SEGURANÇA DA SENHA
        # =================================================
        if not any(caractere.isupper() for caractere in nova_senha):
            return render_template(
                "auth/esqueci_senha.html",
                etapa="nova_senha",
                erro="A senha deve conter uma letra maiúscula.",
            )

        if not any(caractere.islower() for caractere in nova_senha):
            return render_template(
                "auth/esqueci_senha.html",
                etapa="nova_senha",
                erro="A senha deve conter uma letra minúscula.",
            )

        if not any(caractere.isdigit() for caractere in nova_senha):
            return render_template(
                "auth/esqueci_senha.html",
                etapa="nova_senha",
                erro="A senha deve conter um número.",
            )

        caracteres_especiais = "!@#$%^&*()-_=+[]{};:,.?/"
        if not any(caractere in caracteres_especiais for caractere in nova_senha):
            return render_template(
                "auth/esqueci_senha.html",
                etapa="nova_senha",
                erro="A senha deve conter um caractere especial.",
            )

        # =================================================
        # GERAR HASH DA NOVA SENHA
        # =================================================
        senha_hash = generate_password_hash(nova_senha)

        conn = conectar()

        # =================================================
        # ATUALIZAR SENHA E INVALIDAR CÓDIGO
        # =================================================
        conn.execute(
            """
            UPDATE usuarios
            SET senha = ?
            WHERE id = ?
            """,
            (senha_hash, usuario_id),
        )

        conn.execute(
            """
            UPDATE recuperacao_senha
            SET usado = 1
            WHERE id = ?
            """,
            (codigo_id,),
        )

        conn.commit()
        conn.close()

        # =================================================
        # LIMPAR SESSÃO DE RECUPERAÇÃO
        # =================================================
        session.pop("recuperacao_usuario_id", None)
        session.pop("recuperacao_codigo_id", None)

        # =================================================
        # VOLTAR PARA LOGIN
        # =================================================
        return redirect(url_for("auth.login", recuperado=1))

    # =====================================================
    # ETAPA DESCONHECIDA
    # =====================================================
    return redirect(url_for("auth.esqueci_senha"))