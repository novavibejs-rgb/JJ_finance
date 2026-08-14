from banco.conexao import conectar

conn = conectar()
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(socios)")

for coluna in cursor.fetchall():
    print(
        f"Nome: {coluna['name']}"
        f" | Tipo: {coluna['type']}"
    )

conn.close()
