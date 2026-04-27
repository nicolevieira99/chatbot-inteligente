import json
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# DADOS DE TREINAMENTO (melhorados)
frases = [
    # limite
    'quero ver meu limite',
    'consultar limite',
    'aumentar limite',
    'diminuir limite',

    # cartão
    'bloquear cartão',
    'bloquear cartao',
    'cartão de crédito',
    'cartao de credito',
    'cartão de débito',
    'cartao de debito',
    'problema com cartão',
    'problema com cartao',

    # fatura
    'ver fatura',
    'consultar fatura',
    'segunda via da fatura',
    'quando vence a fatura',

    # senha
    'trocar senha',
    'alterar senha',

    # compra
    'compra recusada',
    'problema com compra',

    # parcelamento
    'parcelar fatura',
    'parcelamento',

    # pagamento
    'pagar fatura',
    'pagamento',

    # outros
    'debito automatico',
    'débito automático',

    # cumprimento
    'ola',
    'olá',
    'oi',
    'bom dia',
    'boa tarde',
    'boa noite',
    'hello',    
]

categorias = [
    'limite','limite','limite','limite',
    'cartão','cartão','cartão','cartão','cartão','cartão','cartão','cartão',
    'fatura','fatura','fatura','fatura',
    'senha','senha',
    'compra','compra',
    'parcelamento','parcelamento',
    'pagamento','pagamento',
    'outros','outros',
    'cumprimento','cumprimento','cumprimento','cumprimento','cumprimento','cumprimento','cumprimento'
]

# VETORIZADOR (ignora acentos)
vetorizador = CountVectorizer(strip_accents='ascii')
X = vetorizador.fit_transform(frases)

modelo = MultinomialNB()
modelo.fit(X, categorias)

# RESPOSTAS
with open("respostas.json", "r", encoding="utf-8") as arquivo:
    respostas = json.load(arquivo)

# FUNÇÃO PRINCIPAL
def responder(pergunta):
    pergunta = pergunta.lower()

    X = vetorizador.transform([pergunta])
    categoria_prevista = modelo.predict(X)[0]

    probabilidades = modelo.predict_proba(X)[0]
    maior_probabilidade = max(probabilidades)

    if maior_probabilidade < 0.15:
        return "Desculpe, não entendi sua solicitação."

    resposta = respostas.get(categoria_prevista, "Não entendi.")

    # 🔥 se for lista, escolhe aleatória
    if isinstance(resposta, list):
        return random.choice(resposta)

    return resposta

    # 🔥 limite mais baixo (melhor pra poucos dados)
    if maior_probabilidade < 0.15:
        return "Desculpe, não entendi sua solicitação."

    return respostas.get(categoria_prevista, "Não entendi.")