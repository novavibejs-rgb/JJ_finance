from flask import Blueprint, render_template

from banco import faturamentos as faturamentos
from banco import servicos as servicos
from services import financeiro as finaceiro
from banco import despesas as despesas
from utils.Formata_moeda import moeda


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():

    faturamento = moeda(faturamentos.faturamento_semana())
    reserva = moeda(finaceiro.calcular_reserva())
    lucro = moeda(finaceiro.calcular_lucro())
    somar = moeda(despesas.somar_despesas())

    grafico_faturamento = faturamentos.faturamento_por_dia()

    return render_template(
        "dashboard/index.html",
        faturamento=faturamento,
        fundo_transporte=reserva,
        lucro_liquido=lucro,
        somar=somar,
        grafico_faturamento=grafico_faturamento,
    )