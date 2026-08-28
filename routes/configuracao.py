from flask import Blueprint, render_template, request, redirect, url_for

from banco import configuracao


configuracoes_bp = Blueprint(
    "configuracoes",
    __name__,
    url_prefix="/configuracoes"
)


@configuracoes_bp.route("/", methods=["GET", "POST"])
def index():

    config = configuracao.buscar_configuracao()

    if request.method == "POST":

        nome_empresa = request.form["nome_empresa"]
        telefone = request.form.get("telefone")
        email = request.form.get("email")
        endereco = request.form.get("endereco")
        logo = request.form.get("logo")

        configuracao.atualizar_configuracao(
            config["id"],
            nome_empresa,
            telefone,
            email,
            endereco,
            logo
        )

        return redirect(url_for("configuracoes.index"))

    return render_template(
        "configuracoes/index.html",
        configuracao=config
    )