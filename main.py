from flask import Flask, request
from flask_cors import CORS
import openai
import os

openai.api_key = os.getenv("OPENAI_KEY")
used_words = {'3': [], '4': [], '5': [], '6': [], '7': [], '8': [], '9': []}

app = Flask(__name__)
CORS(app)


def get_word_from_open_ai(language, num):
    system_role = "You are a helpful assistant that answers only a json object containing a random, " \
                  "common word in %s with the number of letters that is sent to you and that same word " \
                  "scrambled. For example: {'word': 'cat', 'scrambledWord': 'tac'}. That word cannot be in " \
                  "this list: %s." % (language, used_words.get(str(num)))

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": system_role},
                  {"role": "user", "content": "Number of letters: %s." % str(num)}],
        temperature=0.9,
    )

    return response['choices'][0]['message']['content']


def getNewWord(data):
    difficulties = {
        "Easy": 3,
        "Medium": 4,
        "Intermediate": 5,
        "Challenging": 6,
        "Hard": 7,
        "Expert": 8,
        "Master": 9
    }
    difficulty = data.get('difficulty')
    num_of_letters = difficulties[difficulty]

    language = data.get('language')

    word_data = get_word_from_open_ai(language, num_of_letters)
    print('Word data: ', word_data)

    word_data_dictionary = eval(word_data)
    print('Word data dictionary: ', word_data)

    used_words.get(str(num_of_letters)).append(word_data_dictionary.get('word'))
    print(used_words)
    return word_data_dictionary


@app.route('/getword', methods=['POST'])
def getWord():
    return getNewWord(request.json)


@app.route('/')
def sayHi():
    return {"word": "tuna", "scrambledWord": "anut"}


if __name__ == '__main__':
    app.run()

# def dif(dif):
#     wordList = []
#     if dif == 1:
#         wordList = ["sob", "vil", "não", "paz", "ser", "mal", "ver", "céu", "ter", "ego", "bem", "vão", "vir", "mãe",
#                     "mas", "dar", "réu", "ora", "bom", "era", "dom", "elo", "são", "tal", "luz", "com", "que", "nós",
#                     "até", "ato", "dia", "pós", "dou", "eis", "pro", "dor", "uma", "pai", "sem", "foi", "irá", "sol",
#                     "por", "pau", "seu", "ler", "mim", "fiz", "ajo", "lei", "tão", "lua", "voo", "rua", "num", "mau",
#                     "nem", "mão", "daí", "rio", "meu", "pôr", "voz", "vez", "fim", "for", "fez", "jus", "ido", "eco",
#                     "via", "sim", "gay", "rei", "amo", "cia", "uns", "tem", "aia", "lhe", "mês", "ira", "olá", "som",
#                     "asa", "sua", "sub", "pré", "azo", "rir"]
#     elif dif == 2:
#         wordList = ["amor", "fato", "viés", "puta", "mito", "esmo", "caos", "brio", "vide", "como", "ação", "após",
#                     "auge", "você", "sede", "pois", "ermo", "ônus", "mote", "vida", "tolo", "saga", "suma", "apto",
#                     "crer", "idem", "medo", "além", "urge", "área", "veio", "zelo", "cota", "pude", "vovó", "ruim",
#                     "ente", "coxo", "casa", "ater", "soar", "sina", "gozo", "fase", "rude", "foda", "rima", "voga",
#                     "pela", "cujo", "auto", "cedo", "mais", "onde", "será", "para", "sela", "meio", "tudo", "teor",
#                     "nojo", "trás", "face", "cela", "ante", "jugo", "logo", "pose", "numa", "base", "asco", "teve",
#                     "alvo", "traz", "amar", "agir", "alva", "meta", "vale", "ócio", "ágil", "peço", "nexo", "eita",
#                     "todo", "doce", "rito", "rege", "alta", "foco", "pelo", "arte", "orla", "deus", "mero", "alto",
#                     "sair", "tese", "irão", "ódio"]
#     elif dif == 3:
#         wordList = ["sagaz", "negro", "âmago", "êxito", "mexer", "termo", "algoz", "senso", "nobre", "plena", "afeto",
#                     "mútua", "ética", "sutil", "audaz", "vigor", "inato", "tênue", "aquém", "porém", "sanar", "seção",
#                     "desde", "fazer", "cerne", "ideia", "moral", "assim", "poder", "torpe", "fosse", "anexo", "honra",
#                     "fútil", "justo", "muito", "razão", "ícone", "mútuo", "lapso", "gozar", "quiçá", "égide", "tange",
#                     "hábil", "expor", "haver", "corja", "posse", "sobre", "pesar", "detém", "ávido", "coser", "ardil",
#                     "prole", "etnia", "digno", "genro", "gleba", "casal", "boçal", "então", "causa", "tenaz", "ânsia",
#                     "dizer", "seara", "dengo", "sonho", "brado", "atroz", "crivo", "ceder", "dever", "tempo", "óbice",
#                     "assaz", "amigo", "ânimo", "denso", "ápice", "saber", "comum", "cozer", "pária", "censo", "culto",
#                     "fugaz", "temor", "sendo", "valha", "mundo", "revés", "vício", "pauta", "neném", "pudor", "forte",
#                     "pífio"]
#     elif dif == 4:
#         wordList = ["exceto", "cínico", "idôneo", "âmbito", "néscio", "índole", "mister", "vereda", "apogeu", "inócuo",
#                     "convém", "sádico", "ênfase", "utopia", "mérito", "alusão", "escopo", "anseio", "casual", "pressa",
#                     "alheio", "infame", "nocivo", "hostil", "exímio", "gentil", "afável", "adorno", "idiota", "legado",
#                     "adesão", "cético", "dádiva", "sóbrio", "paixão", "clichê", "aferir", "astuto", "difuso", "êxtase",
#                     "apreço", "otário", "formal", "limiar", "solene", "sessão", "lábaro", "júbilo", "ocioso", "outrem",
#                     "julgar", "ensejo", "eficaz", "facção", "ímpeto", "hábito", "alento", "escusa", "dispor", "também",
#                     "abster", "glória", "embora", "cessão", "exílio", "perene", "alçada", "lúdico", "safado", "ilação",
#                     "isento", "larica", "acento", "cortês", "nuance", "eximir", "sisudo", "etéreo", "objeto", "receio",
#                     "sanção", "acesso", "cobiça", "avidez", "remoto", "mazela", "cômico", "adágio", "vulgar", "alocar",
#                     "ciente", "fático", "hétero", "buscar", "axioma", "lírico", "asseio", "desejo"]
#     elif dif == 5:
#         wordList = ["empatia", "embuste", "cônjuge", "exceção", "efêmero", "prolixo", "idílico", "caráter", "análogo",
#                     "genuíno", "estória", "sublime", "pêsames", "verbete", "sucinto", "inferir", "audácia", "apático",
#                     "recesso", "astúcia", "pródigo", "acepção", "cinismo", "redimir", "refutar", "estável", "estigma",
#                     "exortar", "família", "cordial", "icônico", "trivial", "mórbido", "escória", "emergir", "imputar",
#                     "síntese", "virtude", "cultura", "aspecto", "soberba", "mitigar", "anátema", "deboche", "candura",
#                     "almejar", "excerto", "frívolo", "luxúria", "litígio", "ademais", "alegria", "oriundo", "através",
#                     "austero", "sucesso", "contudo", "fomento", "sensato", "excesso", "alcunha", "conciso", "ambíguo",
#                     "salutar", "ambição", "exilado", "imersão", "quimera", "modesto", "isenção", "padecer", "parcial",
#                     "notório", "estrupo", "exótico", "auferir", "relação", "estirpe", "ansioso", "colosso", "déspota",
#                     "coragem", "intenso", "emotivo", "difusão", "colapso", "demanda", "inércia", "volátil", "límpido",
#                     "hesitar", "orgulho", "ousadia", "sórdido", "vigente", "indagar", "piedade", "erudito", "profano",
#                     "mancebo"]
#     elif dif == 6:
#         wordList = ["inerente", "peculiar", "denegrir", "respeito", "anuência", "deferido", "genocida", "prudente",
#                     "equidade", "iminente", "invasivo", "alienado", "essência", "extensão", "desgraça", "eminente",
#                     "misógino", "abstrato", "pandemia", "empírico", "premissa", "ardiloso", "reiterar", "conceito",
#                     "passível", "ascensão", "prodígio", "devaneio", "conserto", "apologia", "modéstia", "relativo",
#                     "lascívia", "inserção", "inóspito", "monótono", "analogia", "ativista", "respaldo", "remissão",
#                     "rechaçar", "notívago", "sinônimo", "concerne", "despeito", "alicerce", "medíocre", "talarico",
#                     "destarte", "proceder", "distinto", "abnegado", "elegível", "primazia", "retórica", "demagogo",
#                     "fomentar", "metódico", "consiste", "suscitar", "critério", "desfecho", "perfídia", "sucumbir",
#                     "complexo", "portanto", "escárnio", "vocábulo", "verídico", "singular", "amálgama", "jurídico",
#                     "instigar", "desígnio", "sanidade", "gratidão", "resoluto", "rapariga", "solícito", "expedido",
#                     "paradoxo", "inefável", "insípido", "impávido", "história", "repudiar", "obstante", "refletir",
#                     "emulação", "espectro", "maestria", "processo", "contexto", "prosaico", "paralelo", "comunhão",
#                     "abstrair", "presteza", "prendado", "imanente"]
#     elif dif == 7:
#         wordList = ["perspicaz", "recíproco", "impressão", "concessão", "supérfluo", "escrúpulo", "retificar",
#                     "presunção", "concepção", "implícito", "essencial", "plenitude", "hipócrita", "paradigma",
#                     "corolário", "dicotomia", "hegemonia", "propósito", "ratificar", "esdrúxulo", "hermético",
#                     "incidente", "deliberar", "persuadir", "sapiência", "aleatório", "promíscuo", "resignado",
#                     "vagabundo", "indelével", "demasiado", "mesquinho", "eminência", "altruísmo", "impetuoso",
#                     "esperança", "confiança", "regozijar", "inusitado", "diligente", "desdenhar", "descrição",
#                     "exequível", "analítico", "altruísta", "pretensão", "explícito", "prudência", "autóctone",
#                     "discrição", "compaixão", "dissensão", "fidedigno", "taciturno", "autêntico", "constante",
#                     "supressão", "companhia", "restrição", "resolução", "discorrer", "ordinário", "execrável",
#                     "expressão", "percepção", "imparcial", "adjacente", "nostalgia", "jactância", "subjetivo",
#                     "iminência", "irascível", "sintético", "instância", "interesse", "presságio", "limítrofe",
#                     "estagnado", "ludibriar", "obstinado", "leniência", "consoante", "aquisição", "magnânimo",
#                     "entediado", "pederasta", "empecilho", "desumilde", "autonomia", "suplantar", "relevante",
#                     "ambicioso", "preâmbulo", "pretérito", "convicção", "outrossim", "excedente", "cognitivo",
#                     "salientar", "recíproca"]
#
#     return wordList
#
#
# def randomWord(wordList):
#     if len(wordList) >= 2:
#         randWord = wordList[random.randint(0, len(wordList) - 1)]
#     else:
#         randWord = wordList[0]
#
#     wordList.remove(randWord)
#
#     return randWord, wordList
#
#
# def anagram(randWord):
#     anagram = []
#     indexes = []
#     num = len(randWord)
#     i = 0
#     randWordChar = list(randWord)
#
#     while i < (num):
#
#         index = random.randint(0, num - 1)
#         if (index not in indexes):
#             indexes.append(index)
#             anagram.append(randWord[index])
#             i += 1
#
#     if anagram == randWordChar:
#         anagram.clear()
#         indexes.clear()
#         i = 0
#         while i < (num):
#             index = random.randint(0, num - 1)
#             if (index not in indexes):
#                 indexes.append(index)
#                 anagram.append(randWord[index])
#                 i += 1
#
#     return anagram
#
#
# def userGuess(randWord, lives, points, wordList):
#     win = False
#
#     print("--------------------")
#     print("Vidas => ", lives)
#     print("Pontuação => ", points)
#     print("--------------------")
#     guess = input("Digite seu chute: ")
#
#     while guess != randWord:
#         print("\nOps! Você errou!\n")
#         lives -= 1
#         if lives <= 0:
#             print("\nVocê perdeu!")
#             points = 0
#             print("A palavra original era", randWord)
#             break
#         print("Vidas => ", lives)
#         print("Pontuação => ", points)
#         guess = input("\nTente de novo: ")
#     if lives > 0:
#         print("\nParabéns, você acertou!\n")
#         print("Vidas => ", lives)
#         points += 1
#         print("Pontuação => ", points)
#         if len(wordList) == 0:
#             win = True
#     return lives, points, win
#
#
# def goAgain(lives, points):
#     win = False
#     again = "s"
#     wordList = dif()
#     while again == "s":
#         randomWordList = randomWord(wordList)
#         randWord = randomWordList[0]
#         wordList = randomWordList[1]
#
#         print("--------------------")
#         print("O anagrama:")
#         print(anagram(randWord))
#         data = userGuess(randWord, lives, points, wordList)
#         lives = data[0]
#         points = data[1]
#         if lives <= 0:
#             lives = 5
#         if data[2] == True:
#             print(
#                 "--------------------------------------------------------\nPARABÉNS, VOCÊ VIROU O NÍVEL!\n--------------------------------------------------------")
#             break
#
#         print("\n-----------------------\nGostaria de ir de novo? (s/n)")
#         ans = input()
#         while ans != "n" and ans != "s":
#             print("Responda apenas com 's' ou 'n'.\n-----------------------\nGostaria de ir de novo? (s/n)")
#             ans = input()
#         again = ans
#     return lives, points, win
#
#
# def play():
#     print(
#         "Olá! Bem vindo ao 'troca-letra' #working title#\n\nO objetivo do jogo é decifrar o anagrama na tela. Será que você consegue adivinhar a palavra original?\n\n")
#
#     lives = 5
#     print("Vidas => ", lives)
#     points = 0
#     print("Pontuação => ", points)
#
#     data = goAgain(lives, points)
#     lives = data[0]
#     points = data[1]
#
#     print(
#         "\nQuer trocar de dificuldade ou sair do jogo?\nDigite 'dif' se quiser mudar de dificulade, ou 'sair' para sair do jogo.")
#     answer = input()
#
#     while answer != "dif" and answer != "sair":
#         print(
#             "\nTente de novo!\n\nQuer trocar de dificuldade ou sair do jogo?\nDigite 'dif' se quiser mudar de dificulade, ou 'sair' para sair do jogo.")
#         ans = input()
#
#     while answer == "dif":
#         goAgain(lives, points)
#
#         print(
#             "Quer trocar de dificuldade ou sair do jogo?\nDigite 'dif' se quiser mudar de dificulade, ou 'sair' para sair do jogo.")
#         answer = input()
#     print("Ok, adeus! Obrigado por jogar.")
#     print("Sua pontuação: ", points)
