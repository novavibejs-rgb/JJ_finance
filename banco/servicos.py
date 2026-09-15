from banco.conexao import conectar


def cadastrar_servico(
    cliente,
    servico,
    descricao,
    valor,
    forma_pagamento,
    data,
    ):
    conexao = conectar()

    conexao.execute(
        """
        INSERT INTO servicos (
            cliente,
            servico,
            descricao,
            valor,
            forma_pagamento,
            data
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            cliente,
            servico,
            descricao,
            valor,
            forma_pagamento,
            data,
        ),
    )

    conexao.commit()
    conexao.close()


def listar_servicos():
    conexao = conectar()

    servicos = conexao.execute(
        """
        SELECT
            id,
            cliente,
            servico,
            descricao,
            valor,
            forma_pagamento,
            data
        FROM servicos
        ORDER BY id DESC
        """
    ).fetchall()

    conexao.close()

    return servicos


def buscar_servico_por_id(id):
    conexao = conectar()

    servico = conexao.execute(
        """
        SELECT
            id,
            cliente,
            servico,
            descricao,
            valor,
            forma_pagamento,
            data
        FROM servicos
        WHERE id = %s
        """,
        (id,),
    ).fetchone()

    conexao.close()

    return servico


def atualizar_servico(
    id,
    cliente,
    servico,
    descricao,
    valor,
    forma_pagamento,
    data,
):
    conexao = conectar()

    conexao.execute(
        """
        UPDATE servicos
        SET
            cliente = %s,
            servico = %s,
            descricao = %s,
            valor = %s,
            forma_pagamento = %s,
            data = %s
        WHERE id = %s
        """,
        (
            cliente,
            servico,
            descricao,
            valor,
            forma_pagamento,
            data,
            id,
        ),
    )

    conexao.commit()
    conexao.close()



def excluir_servico(id):
    conexao = conectar()

    conexao.execute(
        """
        DELETE FROM servicos
        WHERE id = %s
        """,
        (id,),
    )

    conexao.commit()
    conexao.close()