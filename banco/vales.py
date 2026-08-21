from banco.conexao import conectar


def cadastrar_vale(
    id_pessoa,
    tipo_pessoa,
    valor,
    descricao,
    inicio_semana,
    fim_semana,
    data,
):
    conexao = conectar()

    conexao.execute(
        """
        INSERT INTO vales (
            id_pessoa,
            tipo_pessoa,
            valor,
            descricao,
            inicio_semana,
            fim_semana,
            data
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            id_pessoa,
            tipo_pessoa,
            valor,
            descricao,
            inicio_semana,
            fim_semana,
            data,
        ),
    )

    conexao.commit()
    conexao.close()


def listar_vales(pesquisa=None):
    conexao = conectar()

    sql = """
        SELECT
            vales.id,
            vales.id_pessoa,
            vales.tipo_pessoa,

            CASE
                WHEN vales.tipo_pessoa = 'socio'
                    THEN socios.nome
                WHEN vales.tipo_pessoa = 'funcionario'
                    THEN funcionarios.nome
            END AS nome,

            vales.valor,
            vales.descricao,
            vales.inicio_semana,
            vales.fim_semana,
            vales.data

        FROM vales

        LEFT JOIN socios
            ON vales.tipo_pessoa = 'socio'
            AND socios.id = vales.id_pessoa

        LEFT JOIN funcionarios
            ON vales.tipo_pessoa = 'funcionario'
            AND funcionarios.id = vales.id_pessoa
    """

    parametros = []

    if pesquisa:
        pesquisa = pesquisa.strip()

        sql += """
            WHERE
                CAST(vales.id_pessoa AS TEXT) LIKE ?
                OR
                (
                    vales.tipo_pessoa = 'socio'
                    AND socios.nome LIKE ?
                )
                OR
                (
                    vales.tipo_pessoa = 'funcionario'
                    AND funcionarios.nome LIKE ?
                )
        """

        termo = f"%{pesquisa}%"

        parametros = [
            termo,
            termo,
            termo,
        ]

    sql += """
        ORDER BY vales.id DESC
    """

    vales = conexao.execute(
        sql,
        parametros,
    ).fetchall()

    conexao.close()

    return vales


def buscar_vale_por_id(id):
    conexao = conectar()

    vale = conexao.execute(
        """
        SELECT
            id,
            id_pessoa,
            tipo_pessoa,
            valor,
            descricao,
            inicio_semana,
            fim_semana,
            data
        FROM vales
        WHERE id = ?
        """,
        (id,),
    ).fetchone()

    conexao.close()

    return vale


def atualizar_vale(
    id,
    id_pessoa,
    tipo_pessoa,
    valor,
    descricao,
    inicio_semana,
    fim_semana,
    data,
):
    conexao = conectar()

    conexao.execute(
        """
        UPDATE vales
        SET
            id_pessoa = ?,
            tipo_pessoa = ?,
            valor = ?,
            descricao = ?,
            inicio_semana = ?,
            fim_semana = ?,
            data = ?
        WHERE id = ?
        """,
        (
            id_pessoa,
            tipo_pessoa,
            valor,
            descricao,
            inicio_semana,
            fim_semana,
            data,
            id,
        ),
    )

    conexao.commit()
    conexao.close()


def excluir_vale(id):
    conexao = conectar()

    conexao.execute(
        """
        DELETE FROM vales
        WHERE id = ?
        """,
        (id,),
    )

    conexao.commit()
    conexao.close()