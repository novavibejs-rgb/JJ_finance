from utils.datas import formatar_data


def registrar_filtros(app):
    app.jinja_env.filters["data"] = formatar_data