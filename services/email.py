import smtplib

from email.message import EmailMessage

from flask import render_template, url_for

from banco.configuracao import (
    buscar_configuracao_email,
    buscar_configuracao
)

def enviar_email(
    destinatario,
    assunto,
    mensagem,
    template_html=None, 
    **contexto
    ):
    configuracao = buscar_configuracao_email()

    if not configuracao:
        return False, "Nenhuma configuração de e-mail cadastrada."

    servidor = None

    try:
        smtp_server = configuracao["smtp_server"]
        smtp_port = int(configuracao["smtp_port"])
        email = configuracao["email"]
        senha = configuracao["senha"]

        email_mensagem = EmailMessage()

        email_mensagem["From"] = email
        email_mensagem["To"] = destinatario
        email_mensagem["Subject"] = assunto

        email_mensagem.set_content(mensagem)

        if template_html:
            html = criar_email_html(
                assunto,
                template_html,
                **contexto
            )

            if html:
                email_mensagem.add_alternative(
                    html,
                    subtype="html"
                )

        servidor = smtplib.SMTP(
            smtp_server,
            smtp_port,
            timeout=10
        )

        servidor.ehlo()
        servidor.starttls()
        servidor.ehlo()

        servidor.login(
            email,
            senha
        )

        servidor.send_message(
            email_mensagem
        )

        return True, "E-mail enviado com sucesso."

    except smtplib.SMTPAuthenticationError:
        return False, (
            "Não foi possível enviar o e-mail. "
            "Verifique o endereço de e-mail e a senha de aplicativo."
        )

    except smtplib.SMTPConnectError:
        return False, (
            "Não foi possível conectar ao servidor de e-mail. "
            "Verifique o servidor SMTP e a porta configurada."
        )

    except (TimeoutError, OSError):
        return False, (
            "Não foi possível conectar ao servidor de e-mail. "
            "Verifique sua conexão e as configurações SMTP."
        )

    except Exception:
        return False, (
            "Não foi possível enviar o e-mail de teste. "
            "Verifique as configurações de e-mail e tente novamente."
        )

    finally:
        if servidor is not None:
            try:
                servidor.quit()
            except Exception:
                pass


def criar_email_html(titulo, template, **contexto):
    configuracao = buscar_configuracao()

    if not configuracao:
        return None

    nome_empresa = configuracao["nome_empresa"]
    telefone = configuracao["telefone"]
    logo = configuracao["logo"]

    logo_url = None

    if logo:
        logo_url = url_for(
            "static",
            filename=logo,
            _external=True
        )

    conteudo = render_template(
        template,
        **contexto
    )

    return render_template(
        "emails/base.html",
        titulo=titulo,
        conteudo=conteudo,
        nome_empresa=nome_empresa,
        telefone=telefone,
        logo=logo_url
    )
