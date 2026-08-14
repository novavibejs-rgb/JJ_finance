from flask import Blueprint, render_template

from banco import socios

socios_bp = Blueprint("socios", __name__)


@socios_bp.route("/socios")
def index():

    lista_socios = socios.listar_socios()

    return render_template(
        "socios/index.html",
        socios=lista_socios
    )

@socios_bp.route("/socios/novo")
def novo():
    return render_template("socios/novo.html")


@socios_bp.route("/socios/editar")
def editar():
    return render_template("socios/editar.html")

@socios_bp.route("/socios/excluir")
def excluir():
    return render_template("socios/excluir.html")