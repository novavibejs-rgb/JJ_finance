from flask import (
Blueprint,
render_template,
request,
redirect,
url_for
)

from banco import vales
from banco import socios
from banco import fucionarios as funcionarios

from utils.datas import intervalo_semana_dt
from utils.auth import somente_admin

vales_bp = Blueprint(
    "vales",
    __name__,
    url_prefix="/vales"
)

# =========================================================

# LISTAR VALES

# =========================================================

@vales_bp.route("/")
@somente_admin
def index():
    
    pesquisa = request.args.get(
        "pesquisa",
        ""
    ).strip()

    lista_vales = vales.listar_vales(
        pesquisa
    )

    return render_template(
        "vales/index.html",
        vales=lista_vales,
        pesquisa=pesquisa
    )


# =========================================================

# NOVO VALE

# =========================================================

@vales_bp.route(
    "/novo",
    methods=["GET", "POST"]
    )

@somente_admin
def novo():


    lista_socios = socios.listar_socios()
    lista_funcionarios = funcionarios.listar_funcionarios()

    if request.method == "POST":

        id_pessoa = request.form["id_pessoa"]
        tipo_pessoa = request.form["tipo_pessoa"]
        valor = request.form["valor"]
        descricao = request.form.get("descricao")
        data = request.form.get("data")

        inicio, fim = intervalo_semana_dt()

        inicio_semana = inicio.strftime(
            "%Y-%m-%d"
        )

        fim_semana = fim.strftime(
            "%Y-%m-%d"
        )

        vales.cadastrar_vale(
            id_pessoa,
            tipo_pessoa,
            valor,
            descricao,
            inicio_semana,
            fim_semana,
            data
        )

        return redirect(
            url_for("vales.index")
        )

    # =====================================================
    # CONVERTER SQLITE ROW PARA DICIONÁRIO
    # =====================================================

    lista_socios_json = [
        {
            "id": socio["id"],
            "nome": socio["nome"]
        }
        for socio in lista_socios
    ]

    lista_funcionarios_json = [
        {
            "id": funcionario["id"],
            "nome": funcionario["nome"]
        }
        for funcionario in lista_funcionarios
    ]

    return render_template(
        "vales/novo.html",
        socios=lista_socios_json,
        funcionarios=lista_funcionarios_json
)


# =========================================================

# EDITAR VALE

# =========================================================

@vales_bp.route("/editar/<int:id>",
    methods=["GET", "POST"]
    )

@somente_admin
def editar(id):
    vale = vales.buscar_vale_por_id(id)

    if not vale:
        return "Vale não encontrado", 404

    lista_socios = socios.listar_socios()
    lista_funcionarios = funcionarios.listar_funcionarios()

    if request.method == "POST":

        id_pessoa = request.form["id_pessoa"]
        tipo_pessoa = request.form["tipo_pessoa"]
        valor = request.form["valor"]
        descricao = request.form.get("descricao")
        data = request.form.get("data")

        inicio, fim = intervalo_semana_dt()

        inicio_semana = inicio.strftime(
            "%Y-%m-%d"
        )

        fim_semana = fim.strftime(
            "%Y-%m-%d"
        )

        vales.atualizar_vale(
            id,
            id_pessoa,
            tipo_pessoa,
            valor,
            descricao,
            inicio_semana,
            fim_semana,
            data
        )

        return redirect(
            url_for("vales.index")
        )

    # =====================================================
    # CONVERTER SOCIOS PARA JSON
    # =====================================================

    lista_socios_json = [
        {
            "id": socio["id"],
            "nome": socio["nome"]
        }
        for socio in lista_socios
    ]

    # =====================================================
    # CONVERTER FUNCIONARIOS PARA JSON
    # =====================================================

    lista_funcionarios_json = [
        {
            "id": funcionario["id"],
            "nome": funcionario["nome"]
        }
        for funcionario in lista_funcionarios
    ]

    return render_template(
        "vales/editar.html",
        vale=vale,
        socios=lista_socios_json,
        funcionarios=lista_funcionarios_json
    )

# =========================================================

# EXCLUIR VALE

# =========================================================

@vales_bp.route("/excluir/<int:id>")

@somente_admin
def excluir(id):
    
    vales.excluir_vale(id)

    return redirect(
        url_for("vales.index")
    )

