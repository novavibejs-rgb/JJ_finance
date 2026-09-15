
from banco.conexao import conectar


# =========================================================
# LISTAR SÓCIOS
# =========================================================

def listar_socios():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            nome,
            email,
            foto,
            telefone,
            status
        FROM socios
        ORDER BY nome
    """)

    socios = cursor.fetchall()

    conexao.close()

    return socios


# =========================================================
# TOTAL DE SÓCIOS
# =========================================================

def total_socios():

    with conectar() as conexao:

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM socios
        """)

        return cursor.fetchone()["total"]


# =========================================================
# BUSCAR SÓCIO POR ID
# =========================================================

def buscar_socio_por_id(id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            nome,
            email,
            foto,
            telefone,
            status
        FROM socios
        WHERE id = %s
    """, (id,))

    socio = cursor.fetchone()

    conexao.close()

    return socio


# =========================================================
# CADASTRAR SÓCIO
# =========================================================

def cadastrar_socio(
    nome,
    email=None,
    foto=None,
    telefone=None
):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO socios (
            nome,
            email,
            foto,
            telefone,
            status
        )
        VALUES (%s, %s, %s, %s, %s)
    """, (
        nome,
        email,
        foto,
        telefone,
        "offline"
    ))

    conexao.commit()

    conexao.close()


# =========================================================
# ATUALIZAR SÓCIO
# =========================================================

def atualizar_socio(
    id,
    nome,
    email=None,
    foto=None,
    telefone=None
):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE socios
        SET
            nome = %s,
            email = %s,
            foto = %s,
            telefone = %s
        WHERE id = %s
    """, (
        nome,
        email,
        foto,
        telefone,
        id
    ))

    conexao.commit()

    conexao.close()


# =========================================================
# ALTERAR STATUS
# =========================================================

def alterar_status_socio(id, status):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE socios
        SET status = %s
        WHERE id = %s
    """, (
        status,
        id
    ))

    conexao.commit()

    conexao.close()


# =========================================================
# EXCLUIR SÓCIO
# =========================================================

def excluir_socio(id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM socios
        WHERE id = %s
    """, (id,))

    conexao.commit()

    conexao.close()