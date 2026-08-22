from flask import Blueprint, render_template, request, redirect, url_for


from banco.fucionarios import (
    listar_funcionarios,
    buscar_funcionario_por_id,
    cadastrar_funcionario,
    atualizar_funcionario,
    excluir_funcionario
)


funcionario_bp = Blueprint("funcionarios", __name__)


# =========================================================
# LISTAR FUNCIONÁRIOS
# =========================================================

@funcionario_bp.route("/funcionarios")
def index():

    lista_funcionarios = listar_funcionarios()

    return render_template(
        "funcionarios/index.html",
        funcionarios=lista_funcionarios
    )


# =========================================================
# NOVO FUNCIONÁRIO
# =========================================================
@funcionario_bp.route("/funcionarios/novo", methods=["GET", "POST"])
def novo():

    if request.method == "POST":

        nome = request.form["nome"]
        cargo = request.form.get("cargo")
        email = request.form.get("email")
        telefone = request.form.get("telefone")
        data_admissao = request.form.get("data_admissao")

        cadastrar_funcionario(
            nome=nome,
            cargo=cargo,
            email=email,
            telefone=telefone,
            data_admissao=data_admissao
        )

        return redirect(
            url_for("funcionarios.index")
        )

    return render_template(
        "funcionarios/novo.html"
    )

# =========================================================
# EDITAR FUNCIONÁRIO
# =========================================================

@funcionario_bp.route(
    "/funcionarios/editar/<int:id>",
    methods=["GET", "POST"]
)
def editar(id):

    funcionario = buscar_funcionario_por_id(id)

    if funcionario is None:
        return "Funcionário não encontrado", 404


    if request.method == "POST":

        nome = request.form["nome"]
        cargo = request.form.get("cargo")
        email = request.form.get("email")
        telefone = request.form.get("telefone")
        data_admissao = request.form.get("data_admissao")

        atualizar_funcionario(
            id=id,
            nome=nome,
            cargo=cargo,
            email=email,
            telefone=telefone,
            data_admissao=data_admissao
        )

        return redirect(
            url_for("funcionarios.index")
        )


    return render_template(
        "funcionarios/editar.html",
        funcionario=funcionario
    )

# =========================================================
# EXCLUIR FUNCIONÁRIO
# =========================================================


@funcionario_bp.route("/funcionarios/excluir/<int:id>")
def excluir(id):

    funcionario = buscar_funcionario_por_id(id)

    if funcionario is None:
        return "Funcionário não encontrado", 404

    excluir_funcionario(id)

    return redirect(
        url_for("funcionarios.index")
    )
