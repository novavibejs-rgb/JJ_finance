from banco.conexao import conectar


def migrar_vales():
    conn = conectar()
    cursor = conn.cursor()

    try:
        print("Iniciando migração da tabela vales...")

        # Verifica se a tabela vales existe
        tabela = cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'vales'
        """).fetchone()

        if not tabela:
            print("A tabela vales não existe.")
            return

        # Verifica as colunas atuais
        colunas = cursor.execute(
            "PRAGMA table_info(vales)"
        ).fetchall()

        nomes_colunas = [coluna["name"] for coluna in colunas]

        # Se já estiver migrada, não faz novamente
        if "id_pessoa" in nomes_colunas and "tipo_pessoa" in nomes_colunas:
            print("A tabela vales já está migrada.")
            return

        print("Estrutura antiga encontrada.")
        print("Criando nova estrutura...")

        # Remove tabela temporária de uma tentativa anterior
        cursor.execute("DROP TABLE IF EXISTS vales_nova")

        # Cria a nova tabela
        #
        # inicio_semana e fim_semana ficam sem NOT NULL
        # porque existem registros antigos que possuem NULL.
        cursor.execute("""
            CREATE TABLE vales_nova (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_pessoa INTEGER NOT NULL,
                tipo_pessoa TEXT NOT NULL,
                valor REAL NOT NULL,
                descricao TEXT,
                inicio_semana TEXT,
                fim_semana TEXT,
                data TEXT
            )
        """)

        # Copia os vales antigos
        #
        # Todo registro antigo é considerado como sendo de um sócio.
        # id_socio passa para id_pessoa.
        cursor.execute("""
            INSERT INTO vales_nova (
                id,
                id_pessoa,
                tipo_pessoa,
                valor,
                descricao,
                inicio_semana,
                fim_semana,
                data
            )
            SELECT
                id,
                id_socio,
                'socio',
                valor,
                descricao,
                inicio_semana,
                fim_semana,
                data
            FROM vales
        """)

        quantidade = cursor.rowcount

        print(f"{quantidade} vale(s) antigo(s) copiado(s).")

        # Confere se a quantidade foi realmente copiada
        quantidade_nova = cursor.execute("""
            SELECT COUNT(*)
            FROM vales_nova
        """).fetchone()[0]

        quantidade_antiga = cursor.execute("""
            SELECT COUNT(*)
            FROM vales
        """).fetchone()[0]

        if quantidade_nova != quantidade_antiga:
            raise Exception(
                "A quantidade de vales copiados não confere."
            )

        # Remove a tabela antiga
        cursor.execute("DROP TABLE vales")

        # Renomeia a nova tabela
        cursor.execute("""
            ALTER TABLE vales_nova
            RENAME TO vales
        """)

        conn.commit()

        print()
        print("======================================")
        print(" MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("======================================")
        print(f"Vales preservados: {quantidade_nova}")
        print("Vales antigos classificados como: socio")
        print("A tabela agora aceita sócios e funcionários.")
        print()

    except Exception as erro:
        conn.rollback()

        print()
        print("======================================")
        print(" ERRO NA MIGRAÇÃO")
        print("======================================")
        print(erro)
        print("Nenhuma alteração foi confirmada.")
        print()

    finally:
        conn.close()


if __name__ == "__main__":
    migrar_vales()