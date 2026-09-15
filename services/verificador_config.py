import logging
import smtplib

from banco.configuracao import buscar_configuracao_email


logger = logging.getLogger(__name__)


def verificar_smtp():

    configuracao = buscar_configuracao_email()

    if not configuracao:
        return (
            False,
            "Nenhuma configuração de e-mail cadastrada."
        )

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

        return (
            True,
            "Conexão com o servidor de e-mail realizada com sucesso."
        )

    except smtplib.SMTPAuthenticationError as erro:

        logger.error(
            "Falha de autenticação SMTP: %s",
            erro
        )

        return (
            False,
            "O servidor de e-mail recusou as credenciais. "
            "Verifique o endereço de e-mail e a senha de aplicativo."
        )

    except smtplib.SMTPConnectError as erro:

        logger.error(
            "Falha ao conectar ao servidor SMTP: %s",
            erro
        )

        return (
            False,
            "Não foi possível conectar ao servidor de e-mail. "
            "Verifique o servidor SMTP e a porta configurada."
        )

    except (TimeoutError, OSError) as erro:

        logger.error(
            "Erro de conexão SMTP: %s",
            erro
        )

        return (
            False,
            "Não foi possível conectar ao servidor de e-mail. "
            "Verifique sua conexão e as configurações SMTP."
        )

    except Exception as erro:

        logger.exception(
            "Erro inesperado ao verificar SMTP."
        )

        return (
            False,
            "Não foi possível verificar a configuração de e-mail. "
            "Tente novamente."
        )

    finally:

        if servidor is not None:

            try:
                servidor.quit()

            except Exception:
                pass