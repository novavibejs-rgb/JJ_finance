from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from banco import servicos

from utils.auth import somente_admin


servicos_bp = Blueprint(
    "servicos",
    __name__,
    url_prefix="/servicos"
)


# =========================================================
# LISTAR SERVIÇOS
# =========================================================

@servicos_bp.route("/")
@somente_admin
def index():

    lista_servicos = servicos.listar_servicos()

    return render_template(
        "servicos/index.html",
        servicos=lista_servicos
    )


# =========================================================
# NOVO SERVIÇO
# =========================================================

@servicos_bp.route(
    "/novo",
    methods=["GET", "POST"]
)
@somente_admin
def novo():

    if request.method == "POST":

        cliente = request.form["cliente"]

        servico = request.form["servico"]

        descricao = request.form.get(
            "descricao"
        )

        valor = request.form["valor"]

        forma_pagamento = request.form.get(
            "forma_pagamento"
        )

        data = request.form.get(
            "data"
        )


        try:
            valor = float(valor)

        except (ValueError, TypeError):
            return "Valor inválido", 400


        servicos.cadastrar_servico(
            cliente,
            servico,
            descricao,
            valor,
            forma_pagamento,
            data
        )


        return redirect(
            url_for("servicos.index")
        )


    return render_template(
        "servicos/novo.html"
    )


# =========================================================
# EDITAR SERVIÇO
# =========================================================

@servicos_bp.route(
    "/editar/<int:id>",
    methods=["GET", "POST"]
)
@somente_admin
def editar(id):

    servico = servicos.buscar_servico_por_id(
        id
    )


    if not servico:
        return (
            "Serviço não encontrado",
            404
        )


    if request.method == "POST":

        cliente = request.form["cliente"]

        nome_servico = request.form["servico"]

        descricao = request.form.get(
            "descricao"
        )

        forma_pagamento = request.form.get(
            "forma_pagamento"
        )

        data = request.form.get(
            "data"
        )

        valor = request.form["valor"]


        try:
            valor = float(valor)

        except (ValueError, TypeError):
            return "Valor inválido", 400


        servicos.atualizar_servico(
            id,
            cliente,
            nome_servico,
            descricao,
            valor,
            forma_pagamento,
            data
        )


        return redirect(
            url_for("servicos.index")
        )


    return render_template(
        "servicos/editar.html",
        servico=servico
    )


# =========================================================
# EXCLUIR SERVIÇO
# =========================================================

@servicos_bp.route(
    "/excluir/<int:id>"
)
@somente_admin
def excluir(id):

    servicos.excluir_servico(
        id
    )


    return redirect(
        url_for("servicos.index")
    )
