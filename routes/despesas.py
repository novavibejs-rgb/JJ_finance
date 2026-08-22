from flask import Blueprint, render_template, request, redirect, url_for

from banco import despesas




despesas_bp = Blueprint("despesas", __name__)


@despesas_bp.route("/despesas")
def index():

    lista_despesas = despesas.listar_despesas()

    return render_template(
        "despesas/index.html",
        despesas=lista_despesas
    )


@despesas_bp.route("/despesas/nova", methods=["GET", "POST"])
def nova():

    if request.method == "POST":

        categoria = request.form["categoria"]
        descricao = request.form["descricao"]
        valor = float(request.form["valor"])
        data = request.form["data"]
        observacao = request.form["observacao"]

        despesas.adicionar_despesa(
            categoria,
            descricao,
            valor,
            data,
            observacao
        )

        return redirect(url_for("despesas.index"))

    return render_template("despesas/nova.html")


@despesas_bp.route("/despesas/excluir/<int:id>")
def excluir(id):

    despesas.excluir_despesa(id)

    return redirect(url_for("despesas.index"))


@despesas_bp.route("/despesas/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    despesa = despesas.buscar_despesa(id)

    if request.method == "POST":

        categoria = request.form["categoria"]
        descricao = request.form["descricao"]
        valor = float(request.form["valor"])
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

        return redirect(url_for("despesas.index"))

    return render_template(
        "despesas/editar.html",
        despesa=despesa
    )