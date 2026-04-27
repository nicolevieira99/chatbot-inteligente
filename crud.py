from conexao import conectar

def inserir_cliente(nome, cpf):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO clientes (nome, cpf) VALUES (?, ?)",
        (nome, cpf)
    )

    conexao.commit()
    conexao.close()

def salvar_mensagem(sessao_id, tipo, mensagem):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO conversas (sessao_id, tipo, mensagem) VALUES (?, ?, ?)",
        (sessao_id, tipo, mensagem)
    )

    conexao.commit()
    conexao.close()

def obter_conversas(sessao_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT tipo, mensagem, timestamp FROM conversas WHERE sessao_id = ? ORDER BY timestamp",
        (sessao_id,)
    )

    conversas = cursor.fetchall()
    conexao.close()
    return conversas