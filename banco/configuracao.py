from banco.conexao import conectar


def buscar_configuracao():

    conexao = conectar()

    configuracao = conexao.execute("""
        SELECT
            id,
            nome_empresa,
            telefone,
            email,
            endereco,
            logo
        FROM configuracao
        LIMIT 1
    """).fetchone()

    conexao.close()

    return configuracao


def criar_configuracao(
    nome_empresa,
    telefone=None,
    email=None,
    endereco=None,
    logo=None
):

    conexao = conectar()

    conexao.execute("""
        INSERT INTO configuracao (
            nome_empresa,
            telefone,
            email,
            endereco,
            logo
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        nome_empresa,
        telefone,
        email,
        endereco,
        logo
    ))

    conexao.commit()
    conexao.close()


def atualizar_configuracao(
    id,
    nome_empresa,
    telefone=None,
    email=None,
    endereco=None,
    logo=None
    ):

    conexao = conectar()

    conexao.execute("""
        UPDATE configuracao
        SET
            nome_empresa = ?,
            telefone = ?,
            email = ?,
            endereco = ?,
            logo = ?
        WHERE id = ?
    """, (
        nome_empresa,
        telefone,
        email,
        endereco,
        logo,
        id
    ))

    conexao.commit()
    conexao.close()