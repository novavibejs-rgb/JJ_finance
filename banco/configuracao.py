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


def buscar_configuracao_email():

    conexao = conectar()

    configuracao_email = conexao.execute("""
        SELECT
            id,
            smtp_server,
            smtp_port,
            email,
            senha,
            ativo,
            data_cadastro
        FROM configuracao_email
        LIMIT 1
    """).fetchone()

    conexao.close()

    return configuracao_email


def salvar_configuracao_email(
    smtp_server,
    smtp_port,
    email,
    senha
    ):

    conexao = conectar()

    conexao.execute("""
        INSERT INTO configuracao_email (
            smtp_server,
            smtp_port,
            email,
            senha
        )
        VALUES (?, ?, ?, ?)
    """, (
        smtp_server,
        smtp_port,
        email,
        senha
    ))

    conexao.commit()
    conexao.close()


def verificador_config():

    conexao = conectar()

    configuracao = conexao.execute("""
        SELECT id
        FROM configuracao_email
        LIMIT 1
    """).fetchone()

    conexao.close()

    return configuracao


def salvar_ou_atualizar_configuracao_email(
    smtp_server,
    smtp_port,
    email,
    senha
    ):

    configuracao = verificador_config()

    if configuracao:

        atualizar_configuracao_email(
            configuracao["id"],
            smtp_server,
            smtp_port,
            email,
            senha
        )

    else:

        salvar_configuracao_email(
            smtp_server,
            smtp_port,
            email,
            senha
        )


def atualizar_configuracao_email(
    id,
    smtp_server,
    smtp_port,
    email,
    senha
):

    conexao = conectar()

    conexao.execute("""
        UPDATE configuracao_email
        SET
            smtp_server = ?,
            smtp_port = ?,
            email = ?,
            senha = ?
        WHERE id = ?
    """, (
        smtp_server,
        smtp_port,
        email,
        senha,
        id
    ))

    conexao.commit()
    conexao.close()