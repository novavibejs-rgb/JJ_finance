from banco.database import conectar


def listar_socios():

    with conectar() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                nome,
                email,
                foto
            FROM socios
            ORDER BY nome
        """)

        return cursor.fetchall()



def total_socios():
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) AS total FROM socios")

        return cursor.fetchone()["total"]

