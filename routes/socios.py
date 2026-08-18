from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from banco import socios


socios_bp = Blueprint("socios", __name__)


# =========================================================
# LISTAR SÓCIOS
# =========================================================

@socios_bp.route("/socios")
def index():

    lista_socios = socios.listar_socios()

    return render_template(
        "socios/index.html",
        socios=lista_socios
    )


# =========================================================
# NOVO SÓCIO
# =========================================================

@socios_bp.route(
    "/socios/novo",
    methods=["GET", "POST"]
)
def novo():

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form.get("email")
        telefone = request.form.get("telefone")
        foto = request.form.get("foto")

        socios.cadastrar_socio(
            nome=nome,
            email=email,
            telefone=telefone,
            foto=foto
        )

        return redirect(
            url_for("socios.index")
        )

    return render_template(
        "socios/novo.html"
    )


# =========================================================
# EDITAR SÓCIO
# =========================================================

@socios_bp.route(
    "/socios/editar/<int:id>",
    methods=["GET", "POST"]
)
def editar(id):

    socio = socios.buscar_socio_por_id(id)

    if socio is None:
        return "Sócio não encontrado", 404


    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form.get("email")
        telefone = request.form.get("telefone")
        foto = request.form.get("foto")

        socios.atualizar_socio(
            id=id,
            nome=nome,
            email=email,
            telefone=telefone,
            foto=foto
        )

        return redirect(
            url_for("socios.index")
        )


    return render_template(
        "socios/editar.html",
        socio=socio
    )


# =========================================================
# EXCLUIR SÓCIO
# =========================================================

@socios_bp.route(
    "/socios/excluir/<int:id>"
)
def excluir(id):

    socio = socios.buscar_socio_por_id(id)

    if socio is None:
        return "Sócio não encontrado", 404

    socios.excluir_socio(id)

    return redirect(
        url_for("socios.index")
    )