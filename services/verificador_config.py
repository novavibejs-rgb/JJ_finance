import smtplib

from banco.configuracao import buscar_configuracao_email


def verificar_smtp():

    configuracao = buscar_configuracao_email()

    if not configuracao:
        return False, "Nenhuma configuração de e-mail cadastrada."

    servidor = None

    try:

        smtp_server = configuracao["smtp_server"]
        smtp_port = int(configuracao["smtp_port"])
        email = configuracao["email"]
        senha = configuracao["senha"]

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

        return True, "Conexão SMTP realizada com sucesso."

    except Exception as erro:

        return False, f"Erro ao conectar ao servidor SMTP: {erro}"

    finally:

        if servidor is not None:

            try:
                servidor.quit()
            except Exception:
                pass