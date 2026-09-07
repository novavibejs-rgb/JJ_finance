from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from banco import despesas

from utils.auth import somente_admin


despesas_bp = Blueprint(
    "despesas",
    __name__
)


# =========================================================
# LISTAR DESPESAS
# =========================================================

@despesas_bp.route("/despesas")
@somente_admin
def index():

    lista_despesas = despesas.listar_despesas()

    return render_template(
        "despesas/index.html",
        despesas=lista_despesas
    )


# =========================================================
# NOVA DESPESA
# =========================================================

@despesas_bp.route(
    "/despesas/nova",
    methods=["GET", "POST"]
)
@somente_admin
def nova():

    if request.method == "POST":

        categoria = request.form["categoria"]

        descricao = request.form["descricao"]

        valor = float(
            request.form["valor"]
        )

        data = request.form["data"]

        observacao = request.form["observacao"]

        despesas.adicionar_despesa(
            categoria,
            descricao,
            valor,
            data,
            observacao
        )

        return redirect(
            url_for("despesas.index")
        )


    return render_template(
        "despesas/nova.html"
    )


# =========================================================
# EXCLUIR DESPESA
# =========================================================

@despesas_bp.route(
    "/despesas/excluir/<int:id>"
)
@somente_admin
def excluir(id):

    despesas.excluir_despesa(
        id
    )

    return redirect(
        url_for("despesas.index")
    )


# =========================================================
# EDITAR DESPESA
# =========================================================

@despesas_bp.route(
    "/despesas/editar/<int:id>",
    methods=["GET", "POST"]
)
@somente_admin
def editar(id):

    despesa = despesas.buscar_despesa(
        id
    )


    if despesa is None:
        return (
            "Despesa não encontrada",
            404
        )


    if request.method == "POST":

        categoria = request.form["categoria"]

        descricao = request.form["descricao"]

        valor = float(
            request.form["valor"]
        )

        data = request.form["data"]

        observacao = request.form["observacao"]

        despesas.atualizar_despesa(
            id,
            categoria,
            descricao,
            valor,
            data,
            observacao
        )

        return redirect(
            url_for("despesas.index")
        )


    return render_template(
        "despesas/editar.html",
        despesa=despesa
    )

