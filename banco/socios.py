from banco.conexao import conectar
from utils.datas import inicio_semana, fim_semana


def listar_socios():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            nome,
            email,
            telefone,
            foto,
            status
        FROM socios
        ORDER BY nome
    """)

    socios = cursor.fetchall()

    conn.close()

    return socios


def total_socios():
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) AS total FROM socios")

        return cursor.fetchone()["total"]

