from flask import session, redirect, url_for, request


ROTAS_PUBLICAS = {
    "auth.login",
    "static",
}


def usuario_logado():
    return bool(session.get("usuario_id"))


def proteger_rotas(app):

    @app.before_request
    def verificar_autenticacao():

        # Permite login e arquivos estáticos
        if request.endpoint in ROTAS_PUBLICAS:
            return None

        # Se não estiver logado
        if not usuario_logado():
            return redirect(url_for("auth.login"))

        return None