from banco.conexao import conectar


def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # =========================================================
    # SÓCIOS
    # =========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS socios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT,
        foto TEXT,
        telefone TEXT,
        status TEXT NOT NULL DEFAULT 'online'
    )
    """)

    # =========================================================
    # SERVIÇOS
    # =========================================================

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

    # =========================================================
    # VALES
    # =========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vales (
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

    # =========================================================
    # CONFIGURAÇÃO DE E-MAIL
    # =========================================================

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

    # =========================================================
    # DESPESAS DA EMPRESA
    # =========================================================

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

    # =========================================================
    # FUNCIONÁRIOS
    # =========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS funcionarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cargo TEXT,
        email TEXT,
        telefone TEXT,
        foto TEXT,
        status TEXT NOT NULL DEFAULT 'online',
        data_admissao TEXT
    )
    """)

    # =========================================================
    # USUÁRIOS
    # =========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        usuario TEXT NOT NULL UNIQUE,
        email TEXT UNIQUE,
        senha TEXT NOT NULL,
        nivel TEXT NOT NULL DEFAULT 'admin',
        ativo INTEGER NOT NULL DEFAULT 1,
        data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =========================================================
    # MIGRAÇÃO DA TABELA USUÁRIOS
    # =========================================================

    cursor.execute("""
        PRAGMA table_info(usuarios)
    """)

    colunas_usuarios = [
        coluna[1]
        for coluna in cursor.fetchall()
    ]

    if "email" not in colunas_usuarios:
        cursor.execute("""
            ALTER TABLE usuarios
            ADD COLUMN email TEXT
        """)

    # =========================================================
    # CONFIGURAÇÃO DA EMPRESA
    # =========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS configuracao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_empresa TEXT NOT NULL,
        telefone TEXT,
        email TEXT,
        endereco TEXT,
        logo TEXT
    )
    """)

    # =========================================================
    # RECUPERAÇÃO DE SENHA
    # =========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recuperacao_senha (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        codigo_hash TEXT NOT NULL,
        expiracao DATETIME NOT NULL,
        tentativas INTEGER NOT NULL DEFAULT 0,
        usado INTEGER NOT NULL DEFAULT 0,
        criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()