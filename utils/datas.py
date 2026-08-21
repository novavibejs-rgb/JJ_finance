from datetime import datetime, timedelta


def intervalo_semana_dt():
    """
    Retorna início e fim da semana como datetime.
    """

    hoje = datetime.now()

    inicio = hoje - timedelta(days=hoje.weekday())

    inicio = inicio.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    fim = inicio + timedelta(days=6)

    fim = fim.replace(
        hour=23,
        minute=59,
        second=59,
        microsecond=999999
    )

    return inicio, fim


def inicio_semana():
    """
    Retorna o início da semana.
    """
    return intervalo_semana_dt()[0]


def fim_semana():
    """
    Retorna o fim da semana.
    """
    return intervalo_semana_dt()[1]


def formatar_data(data):
    """
    Formata a data vinda do banco.

    Banco:
        2026-07-23 22:32:03

    Exibição:
        23/07/2026
    """

    if not data:
        return ""

    if isinstance(data, datetime):
        return data.strftime("%d/%m/%Y")

    try:
        data = datetime.strptime(
            str(data),
            "%Y-%m-%d %H:%M:%S"
        )

        return data.strftime("%d/%m/%Y")

    except ValueError:
        return str(data)