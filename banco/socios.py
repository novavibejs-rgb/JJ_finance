
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
        WHERE id = ?
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
        VALUES (?, ?, ?, ?, ?)
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
            nome = ?,
            email = ?,
            foto = ?,
            telefone = ?
        WHERE id = ?
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
        SET status = ?
        WHERE id = ?
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
        WHERE id = ?
    """, (id,))

    conexao.commit()

    conexao.close()