from banco.conexao import conectar
from utils.datas import inicio_semana, fim_semana


def faturamento_semana():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(valor)
        FROM servicos
        WHERE data BETWEEN ? AND ?
    """, (
        inicio_semana(),
        fim_semana()
    ))

    total = cursor.fetchone()[0]

    conn.close()

    return total if total else 0