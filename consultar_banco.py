import sqlite3

def consultar_banco():
    """Consulta direta no banco de dados"""
    conexao = sqlite3.connect('banco.db')
    cursor = conexao.cursor()

    print("=== CONSULTA DIRETA NO BANCO ===\n")

    # Ver tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = cursor.fetchall()
    print("📋 Tabelas no banco:")
    for tabela in tabelas:
        print(f"  • {tabela[0]}")

    print()

    # Ver estrutura das tabelas
    for tabela in tabelas:
        nome_tabela = tabela[0]
        print(f"📊 Estrutura da tabela '{nome_tabela}':")
        cursor.execute(f"PRAGMA table_info({nome_tabela})")
        colunas = cursor.fetchall()
        for col in colunas:
            print(f"  • {col[1]} ({col[2]})")
        print()

        # Ver dados (últimas 10 linhas)
        try:
            cursor.execute(f"SELECT * FROM {nome_tabela} ORDER BY id DESC LIMIT 10")
            dados = cursor.fetchall()
            if dados:
                print(f"📝 Últimos registros em '{nome_tabela}':")
                for linha in dados:
                    print(f"  • {linha}")
            else:
                print(f"📭 Tabela '{nome_tabela}' está vazia")
        except sqlite3.OperationalError:
            # Se não tem coluna 'id', tenta sem ORDER BY
            try:
                cursor.execute(f"SELECT * FROM {nome_tabela} LIMIT 10")
                dados = cursor.fetchall()
                if dados:
                    print(f"📝 Registros em '{nome_tabela}':")
                    for linha in dados:
                        print(f"  • {linha}")
                else:
                    print(f"📭 Tabela '{nome_tabela}' está vazia")
            except:
                print(f"❌ Erro ao consultar tabela '{nome_tabela}'")
        print()

    conexao.close()

if __name__ == "__main__":
    consultar_banco()