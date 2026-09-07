from banco.conexao import conectar
from utils.datas import inicio_semana, fim_semana
from datetime import timedelta


def faturamento_semana():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(valor)
        FROM servicos
        WHERE data BETWEEN ? AND ?
    """, (
        inicio_semana().strftime("%Y-%m-%d"),
        fim_semana().strftime("%Y-%m-%d")
    ))

    total = cursor.fetchone()[0]

    conn.close()

    return total if total else 0


def faturamento_por_dia():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            data,
            SUM(valor) AS total
        FROM servicos
        WHERE data BETWEEN ? AND ?
        GROUP BY data
        ORDER BY data
    """, (
        inicio_semana().strftime("%Y-%m-%d"),
        fim_semana().strftime("%Y-%m-%d")
    ))

    resultados = cursor.fetchall()

    conn.close()

    # Cria um dicionário com o faturamento de cada data
    faturamento = {
        resultado["data"]: resultado["total"]
        for resultado in resultados
    }

    # Dias da semana
    nomes_dias = [
        "SEG",
        "TER",
        "QUA",
        "QUI",
        "SEX",
        "SÁB",
        "DOM"
    ]

    inicio = inicio_semana()

    dados = []

    for i in range(7):

        data = inicio + timedelta(days=i)

        data_str = data.strftime("%Y-%m-%d")

        dados.append({
            "dia": nomes_dias[i],
            "data": data_str,
            "total": faturamento.get(data_str, 0)
        })

    return dados