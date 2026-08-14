from banco.conexao import conectar

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS socios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT,
        foto TEXT
        
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS servicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT NOT NULL,
        servico TEXT NOT NULL,
        descricao TEXT,
        valor REAL NOT NULL,
        forma_pagamento TEXT,
        data TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_socio INTEGER NOT NULL,
        valor REAL NOT NULL,
        descricao TEXT,
        inicio_semana TEXT NOT NULL,
        fim_semana TEXT NOT NULL,
        data TEXT,
        FOREIGN KEY (id_socio) REFERENCES socios(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS configuracao_email (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        smtp_server TEXT NOT NULL,
        smtp_port INTEGER NOT NULL,
        email TEXT NOT NULL,
        senha TEXT NOT NULL,
        ativo INTEGER DEFAULT 1,
        data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS despesas_empresa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria TEXT NOT NULL,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL,
        data TEXT NOT NULL,
        observacao TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS funcionarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cargo TEXT,
        email TEXT,
        telefone TEXT,
        foto TEXT,
        status TEXT NOT NULL DEFAULT 'offline',
        data_admissao TEXT
    )
    """)


    conn.commit()
    conn.close()

