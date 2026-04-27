import sqlite3
from datetime import datetime

def ver_conversas():
    """Mostra todas as conversas salvas no banco"""
    conexao = sqlite3.connect('banco.db')
    cursor = conexao.cursor()

    # Busca todas as conversas agrupadas por sessão
    cursor.execute("""
        SELECT sessao_id, tipo, mensagem, timestamp
        FROM conversas
        ORDER BY sessao_id, timestamp
    """)

    conversas = cursor.fetchall()
    conexao.close()

    if not conversas:
        print("📭 Nenhuma conversa encontrada no banco.")
        return

    print("💬 CONVERSAS SALVAS NO BANCO:\n")

    sessao_atual = None
    for sessao_id, tipo, mensagem, timestamp in conversas:
        if sessao_atual != sessao_id:
            if sessao_atual is not None:
                print()  # Linha em branco entre sessões
            print(f"🔹 Sessão: {sessao_id[:8]}...")
            sessao_atual = sessao_id

        # Formata o timestamp
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        hora = dt.strftime('%H:%M:%S')

        # Mostra a mensagem
        if tipo == 'usuario':
            print(f"  👤 [{hora}] {mensagem}")
        else:
            print(f"  🤖 [{hora}] {mensagem}")

def ver_estatisticas():
    """Mostra estatísticas das conversas"""
    conexao = sqlite3.connect('banco.db')
    cursor = conexao.cursor()

    # Conta total de mensagens
    cursor.execute("SELECT COUNT(*) FROM conversas")
    total_msgs = cursor.fetchone()[0]

    # Conta mensagens por tipo
    cursor.execute("SELECT tipo, COUNT(*) FROM conversas GROUP BY tipo")
    tipos = cursor.fetchall()

    # Conta sessões únicas
    cursor.execute("SELECT COUNT(DISTINCT sessao_id) FROM conversas")
    sessoes = cursor.fetchone()[0]

    conexao.close()

    print("📊 ESTATÍSTICAS DO CHATBOT:")
    print(f"  💬 Total de mensagens: {total_msgs}")
    print(f"  👥 Sessões únicas: {sessoes}")

    for tipo, count in tipos:
        emoji = "👤" if tipo == "usuario" else "🤖"
        print(f"  {emoji} Mensagens {tipo}: {count}")

if __name__ == "__main__":
    print("=== VISUALIZADOR DE CONVERSAS DO CHATBOT ===\n")
    ver_estatisticas()
    print()
    ver_conversas()