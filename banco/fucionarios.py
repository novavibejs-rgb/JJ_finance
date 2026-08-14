from banco.conexao import conectar


# =========================================================
# LISTAR FUNCIONÁRIOS
# =========================================================

def listar_funcionarios():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM funcionarios
        ORDER BY id DESC
    """)

    funcionarios = cursor.fetchall()

    conexao.close()

    return funcionarios


# =========================================================
# BUSCAR FUNCIONÁRIO POR ID
# =========================================================

def buscar_funcionario_por_id(id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM funcionarios
        WHERE id = ?
    """, (id,))

    funcionario = cursor.fetchone()

    conexao.close()

    return funcionario


# =========================================================
# CADASTRAR FUNCIONÁRIO
# =========================================================

def cadastrar_funcionario(
    nome,
    cargo,
    email=None,
    telefone=None,
    foto=None,
    data_admissao=None
):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO funcionarios (
            nome,
            cargo,
            email,
            telefone,
            foto,
            status,
            data_admissao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        nome,
        cargo,
        email,
        telefone,
        foto,
        "offline",
        data_admissao
    ))

    conexao.commit()

    conexao.close()


# =========================================================
# ATUALIZAR FUNCIONÁRIO
# =========================================================

def atualizar_funcionario(
    id,
    nome,
    cargo,
    email=None,
    telefone=None,
    foto=None,
    data_admissao=None
):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE funcionarios
        SET
            nome = ?,
            cargo = ?,
            email = ?,
            telefone = ?,
            foto = ?,
            data_admissao = ?
        WHERE id = ?
    """, (
        nome,
        cargo,
        email,
        telefone,
        foto,
        data_admissao,
        id
    ))

    conexao.commit()

    conexao.close()


# =========================================================
# ALTERAR STATUS
# =========================================================

def alterar_status_funcionario(id, status):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE funcionarios
        SET status = ?
        WHERE id = ?
    """, (
        status,
        id
    ))

    conexao.commit()

    conexao.close()


# =========================================================
# EXCLUIR FUNCIONÁRIO
# =========================================================

def excluir_funcionario(id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM funcionarios
        WHERE id = ?
    """, (id,))

    conexao.commit()

    conexao.close()