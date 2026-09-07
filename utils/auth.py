from functools import wraps

from flask import (
    session,
    redirect,
    url_for,
    request
)


# ============================================================
# ROTAS PÚBLICAS
# ============================================================

ROTAS_PUBLICAS = {
    "auth.login",
    "auth.esqueci_senha",
    "static"
}


# ============================================================
# VERIFICA SE O USUÁRIO ESTÁ LOGADO
# ============================================================

def usuario_logado():
    return bool(
        session.get("usuario_id")
    )


# ============================================================
# VERIFICA SE O USUÁRIO É ADMIN
# ============================================================

def usuario_admin():
    return (
        usuario_logado()
        and session.get("nivel") == "admin"
    )


# ============================================================
# PROTEÇÃO GERAL DAS ROTAS
# ============================================================

def proteger_rotas(app):

    @app.before_request
    def verificar_autenticacao():

        # Permite acesso às rotas públicas
        if request.endpoint in ROTAS_PUBLICAS:
            return None

        # Usuário não está logado
        if not usuario_logado():
            return redirect(
                url_for("auth.login")
            )

        # Usuário está logado
        return None


# ============================================================
# PROTEÇÃO EXCLUSIVA PARA ADMIN
# ============================================================

def somente_admin(funcao):

    @wraps(funcao)
    def verificar_permissao(*args, **kwargs):

        # Não está logado
        if not usuario_logado():
            return redirect(
                url_for("auth.login")
            )

        # Está logado, mas não é administrador
        if not usuario_admin():
            return (
                "Acesso não autorizado.",
                403
            )

        # É administrador
        return funcao(*args, **kwargs)

    return verificar_permissao

