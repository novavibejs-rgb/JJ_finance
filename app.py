from flask import Flask
from banco.criar_tabelas import criar_tabelas

from config import Config
from routes.dashboard import dashboard_bp
from routes.despesas import despesas_bp

app = Flask(__name__)
app.config.from_object(Config)
criar_tabelas()

app.register_blueprint(dashboard_bp)

app.register_blueprint(despesas_bp)



if __name__ == "__main__":
    app.run(debug=True)