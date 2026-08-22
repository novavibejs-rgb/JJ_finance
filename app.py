from flask import Flask

from banco.criar_tabelas import criar_tabelas

from config import Config

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.despesas import despesas_bp
from routes.socios import socios_bp
from routes.funicionario import funcionario_bp
from routes.servicos import servicos_bp
from routes.vales import vales_bp
from utils.auth import proteger_rotas
from utils.filtros import registrar_filtros


app = Flask(__name__)

app.config.from_object(Config)


criar_tabelas()

proteger_rotas(app)

registrar_filtros(app)


# =========================================================
# ROTAS
# =========================================================

app.register_blueprint(auth_bp)

app.register_blueprint(dashboard_bp)
app.register_blueprint(despesas_bp)
app.register_blueprint(socios_bp)
app.register_blueprint(funcionario_bp)
app.register_blueprint(servicos_bp)
app.register_blueprint(vales_bp)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )