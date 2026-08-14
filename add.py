from banco.conexao import conectar


def atualizar_tabela_socios():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    ALTER TABLE socios
    ADD COLUMN telefone TEXT
    """)

    cursor.execute("""
    ALTER TABLE socios
    ADD COLUMN status TEXT NOT NULL DEFAULT 'online'
    """)

    conn.commit()
    conn.close()

    print("Tabela socios atualizada com sucesso!")

if __name__ == "__main__":
    atualizar_tabela_socios()