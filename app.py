from flask import Flask, request, jsonify, render_template, session
from chatbot import responder
from crud import salvar_mensagem, obter_conversas
import uuid

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # pode deixar assim por enquanto

@app.route("/")
def index():
    # cria sessão única para cada usuário
    if 'sessao_id' not in session:
        session['sessao_id'] = str(uuid.uuid4())
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    dados = request.get_json()
    pergunta = dados.get("mensagem", "")

    sessao_id = session.get('sessao_id', 'anonima')

    # salva mensagem do usuário
    salvar_mensagem(sessao_id, 'usuario', pergunta)

    # 🔥 CORREÇÃO AQUI
    resposta = responder(pergunta)

    # salva resposta do bot
    salvar_mensagem(sessao_id, 'bot', resposta)

    return jsonify({"resposta": resposta})

@app.route("/historico", methods=["GET"])
def historico():
    sessao_id = session.get('sessao_id', 'anonima')
    conversas = obter_conversas(sessao_id)

    return jsonify({
        "conversas": [
            {"tipo": c[0], "mensagem": c[1], "timestamp": c[2]}
            for c in conversas
        ]
    })

if __name__ == "__main__":
    app.run(debug=True)