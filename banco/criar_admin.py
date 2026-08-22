from banco.conexao import conectar
from werkzeug.security import generate_password_hash


def criar_admin():

    nome = "Administrador"
    usuario = "admin"
    senha = "1234"

    senha_hash = generate_password_hash(senha)

    conn = conectar()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO usuarios (
                nome,
                usuario,
                senha,
                nivel,
                ativo
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            nome,
            usuario,
            senha_hash,
            "admin",
            1
        ))

        conn.commit()

        print("✅ Usuário administrador criado com sucesso!")
        print("Usuário:", usuario)
        print("Senha:", senha)

    except Exception as erro:

        conn.rollback()

        print("❌ Erro ao criar administrador:")
        print(erro)

    finally:

        conn.close()


if __name__ == "__main__":
    criar_admin()