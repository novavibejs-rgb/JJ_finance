from banco.conexao import conectar


def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # SOCIOS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS socios (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            email TEXT,
            foto TEXT,
            telefone TEXT,
            status TEXT NOT NULL DEFAULT 'online'
        )
    """)

    # SERVICOS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicos (
            id SERIAL PRIMARY KEY,
            cliente TEXT NOT NULL,
            servico TEXT NOT NULL,
            descricao TEXT,
            valor DOUBLE PRECISION NOT NULL,
            forma_pagamento TEXT,
            data TEXT
        )
    """)

    # VALES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vales (
            id SERIAL PRIMARY KEY,
            id_pessoa INTEGER NOT NULL,
            tipo_pessoa TEXT NOT NULL,
            valor DOUBLE PRECISION NOT NULL,
            descricao TEXT,
            inicio_semana TEXT,
            fim_semana TEXT,
            data TEXT
        )
    """)

    # CONFIGURACAO EMAIL
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS configuracao_email (
            id SERIAL PRIMARY KEY,
            smtp_server TEXT NOT NULL,
            smtp_port INTEGER NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL,
            ativo INTEGER DEFAULT 1,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # DESPESAS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS despesas_empresa (
            id SERIAL PRIMARY KEY,
            categoria TEXT NOT NULL,
            descricao TEXT NOT NULL,
            valor DOUBLE PRECISION NOT NULL,
            data TEXT NOT NULL,
            observacao TEXT
        )
    """)

    # FUNCIONARIOS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS funcionarios (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            cargo TEXT,
            email TEXT,
            telefone TEXT,
            foto TEXT,
            status TEXT NOT NULL DEFAULT 'online',
            data_admissao TEXT
        )
    """)

    # USUARIOS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            usuario TEXT NOT NULL UNIQUE,
            email TEXT UNIQUE,
            senha TEXT NOT NULL,
            nivel TEXT NOT NULL DEFAULT 'admin',
            ativo INTEGER NOT NULL DEFAULT 1,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # CONFIGURACAO EMPRESA
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS configuracao (
            id SERIAL PRIMARY KEY,
            nome_empresa TEXT NOT NULL,
            telefone TEXT,
            email TEXT,
            endereco TEXT,
            logo TEXT
        )
    """)

    # RECUPERACAO SENHA
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recuperacao_senha (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER NOT NULL,
            codigo_hash TEXT NOT NULL,
            expiracao TIMESTAMP NOT NULL,
            tentativas INTEGER NOT NULL DEFAULT 0,
            usado INTEGER NOT NULL DEFAULT 0,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()