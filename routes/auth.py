from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash

from banco.conexao import conectar


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# =========================================================
# LOGIN
# =========================================================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    # Se já estiver logado, não precisa mostrar o login novamente
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

            usuario_db = conn.execute("""
                SELECT *
                FROM usuarios
                WHERE usuario = ?
                  AND ativo = 1
                LIMIT 1
            """, (usuario,)).fetchone()

            conn.close()

            if usuario_db and check_password_hash(
                usuario_db["senha"],
                senha
            ):

                session.clear()

                session["usuario_id"] = usuario_db["id"]
                session["usuario_nome"] = usuario_db["nome"]
                session["usuario"] = usuario_db["usuario"]
                session["nivel"] = usuario_db["nivel"]

                return redirect(url_for("dashboard.index"))

            erro = "Usuário ou senha incorretos."

    return render_template(
        "auth/login.html",
        erro=erro
    )


# =========================================================
# LOGOUT
# =========================================================

@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("auth.login"))