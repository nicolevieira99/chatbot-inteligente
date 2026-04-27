import json
import random
import re
from datetime import datetime
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
    # nome do usuário
    'me chame de joão',
    'me chame de maria',
    'meu nome é joão',
    'meu nome é maria',
    'meu nome e joão',
    'meu nome e maria',
    'eu sou joão',
    'eu sou maria',
    'sou joão',
    'sou maria',
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
    'cumprimento','cumprimento','cumprimento','cumprimento','cumprimento','cumprimento','cumprimento',
    'nome','nome','nome','nome','nome','nome','nome','nome','nome','nome'
]

# VETORIZADOR (ignora acentos)
vetorizador = CountVectorizer(strip_accents='ascii')
X = vetorizador.fit_transform(frases)

modelo = MultinomialNB()
modelo.fit(X, categorias)

# RESPOSTAS
with open("respostas.json", "r", encoding="utf-8") as arquivo:
    respostas = json.load(arquivo)

# Funções auxiliares

def extrair_nome(pergunta):
    padrões = [
        r"me chame de\s+(.+)",
        r"me chame como\s+(.+)",
        r"pode me chamar de\s+(.+)",
        r"meu nome é\s+(.+)",
        r"meu nome e\s+(.+)",
        r"eu sou\s+(.+)",
        r"sou\s+(.+)"
    ]
    for padrão in padrões:
        correspondência = re.search(padrão, pergunta, re.IGNORECASE)
        if correspondência:
            nome = correspondência.group(1).strip()
            nome = re.sub(r"[^\w\sáàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ-]", "", nome)
            return nome.title()
    return None

# FUNÇÃO PRINCIPAL
def responder(pergunta):
    pergunta = pergunta.lower()

    X = vetorizador.transform([pergunta])
    categoria_prevista = modelo.predict(X)[0]

    probabilidades = modelo.predict_proba(X)[0]
    maior_probabilidade = max(probabilidades)

    if maior_probabilidade < 0.15:
        return "Desculpe, não entendi sua solicitação."

    # Ajusta cumprimentos com base no horário
    if categoria_prevista == 'cumprimento':
        resposta_cumprimento = respostas.get('cumprimento')
        if resposta_cumprimento:
            return random.choice(resposta_cumprimento)
        return 'Olá! Como posso ajudá-lo hoje?'

    resposta = respostas.get(categoria_prevista, "Não entendi.")

    # 🔥 se for lista, escolhe aleatória
    if isinstance(resposta, list):
        return random.choice(resposta)

    return resposta