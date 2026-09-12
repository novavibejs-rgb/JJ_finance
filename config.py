import os

class Config:


    # =========================================================
    # CHAVE SECRETA
    # =========================================================

    SECRET_KEY = os.environ.get("SECRET_KEY")

    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY não configurada."
        )


    # =========================================================
    # SEGURANÇA DA SESSÃO
    # =========================================================

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SAMESITE = "Lax"

    SESSION_COOKIE_SECURE = os.environ.get("FLASK_ENV") == "production"

