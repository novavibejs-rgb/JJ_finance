from flask import Blueprint, render_template

from banco.socios import listar_socios, total_socios

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def index():

    socios = listar_socios()
    quantidade_socios = total_socios()

    return render_template(
        "dashboard/index.html",
        socios=socios,
        total_socios=quantidade_socios
    )