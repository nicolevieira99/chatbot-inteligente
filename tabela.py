import sqlite3

# conexão com o banco
conexao = sqlite3.connect('banco.db')
cursor = conexao.cursor()

# criação da tabela
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL UNIQUE,
    numero_cartao TEXT NOT NULL,
    limite_total REAL NOT NULL,
    limite_disponivel REAL NOT NULL,
    fatura_atual REAL NOT NULL,
    vencimento_cartao TEXT NOT NULL,
    vencimento_fatura TEXT NOT NULL,
    status_cartao TEXT NOT NULL
)
""")

# criação da tabela de conversas
cursor.execute("""
CREATE TABLE IF NOT EXISTS conversas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sessao_id TEXT NOT NULL,
    tipo TEXT NOT NULL, -- 'usuario' ou 'bot'
    mensagem TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# salvar alterações
conexao.commit()

# fechar conexão
conexao.close()