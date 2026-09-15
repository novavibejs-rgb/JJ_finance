from banco.conexao import conectar
from utils.datas import inicio_semana

def adicionar_despesa(categoria, descricao, valor, data, observacao):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO despesas_empresa
        (categoria, descricao, valor, data, observacao)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        categoria,
        descricao,
        valor,
        data,
        observacao
    ))

    conn.commit()
    conn.close()


def listar_despesas():
    
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            id,
            categoria,
            descricao,
            valor,
            data,
            observacao
        FROM despesas_empresa
        ORDER BY data DESC
    """)

    despesas = cursor.fetchall()

    conn.close()

    return despesas


def somar_despesas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(valor), 0) AS total
        FROM despesas_empresa
        WHERE data >= %s
    """, (
        inicio_semana().strftime("%Y-%m-%d"),
    ))

    total = cursor.fetchone()["total"]

    conn.close()
    return total


def buscar_despesa (id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            categoria,
            descricao,
            valor,
            data,
            observacao
        FROM despesas_empresa
        WHERE id = %s
    """, (id,))

    despesa = cursor.fetchone()

    conn.close()

    return despesa


def atualizar_despesa(id, categoria, descricao, valor, data, observacao):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE despesas_empresa
        SET
            categoria = %s,
            descricao = %s,
            valor = %s,
            data = %s,
            observacao = %s
        WHERE id = %s
    """, (
        categoria,
        descricao,
        valor,
        data,
        observacao,
        id
    ))

    conn.commit()
    conn.close()


def excluir_despesa(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM despesas_empresa
        WHERE id = %s
    """, (id,))

    conn.commit()
    conn.close()