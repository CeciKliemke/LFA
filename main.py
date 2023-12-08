import re
from sympy import sympify, SympifyError

def criar_automato():
    # Definindo os estados e transições do autômato
    estados = {
        'q0': 0,
        'q1': 1,
        'q2': 2,
        'q3': 3,
        'q4': 4,
        'q5': 5
    }

    transicoes = {
        0: {'letra': 1},
        1: {'letra': 1, 'digito': 1, '_': 1, 'espaco': 2},
        2: {'espaco': 2, '=': 3},
        3: {'digito': 4, 'letra': 4, 'espaco': 3},
        4: {'digito': 4, 'letra': 4, 'op_arit': 4, 'pv': 5, 'espaco': 5},
        5: {'espaco': 5},
    }

    return estados, transicoes

def automato_atribuicao(expressao, estados, transicoes):
    # Removendo espaços em branco no início da expressão
    expressao = expressao.lstrip()

    # Verificando se a expressão começa com um identificador
    if not expressao or not expressao[0].isalpha() or not expressao[0].islower():
        raise ValueError("A expressão deve começar com um identificador.")

    estado_atual = estados['q0']
    for char in expressao:
        if estado_atual == estados['q5']:
            break

        categoria = obter_categoria(char)

        # Verificando se a transição é válida
        if estado_atual not in transicoes or categoria not in transicoes[estado_atual]:
            raise ValueError(f"Transição inválida do estado {estado_atual} com o caractere {char}")

        estado_atual = transicoes[estado_atual][categoria]

    # Verificando se a expressão termina com ponto e vírgula
    if expressao.strip()[-1] != ';':
        raise ValueError("A expressão deve terminar com ponto e vírgula (;)")

    return estado_atual == estados['q5']

def obter_categoria(char):
    # Determinando a categoria do caractere
    if char.islower():  # Verifica se é uma letra minúscula
        return 'letra'
    elif char.isdigit():
        return 'digito'
    elif char == '_':
        return '_'
    elif char == '=':
        return '='
    elif char in ('+', '-', '*', '/'):
        return 'op_arit'
    elif char == ';':
        return 'pv'
    elif char.isspace():
        return 'espaco'
    else:
        raise ValueError(f"Caractere inválido na expressão: {char}")

def avaliar_atribuicao(expressao):
    # Dividindo as linhas da expressão
    linhas = expressao.split('\n')

    identificadores = {}
    for linha in linhas[:-1]:
        # Processando as linhas exceto a última
        if '=' in linha:
            nome, valor = linha.split('=')
            identificadores[nome.strip()] = float(valor.strip())

    # A última linha é a atribuição
    atribuicao = linhas[-1]

    # Verificando se a atribuição começa com um identificador válido
    if not atribuicao or not atribuicao[0].isalpha() or not atribuicao[0].islower():
        raise ValueError("A atribuição deve começar com um identificador.")

    # Removendo o identificador e o sinal de igual da atribuição
    atribuicao = atribuicao.split('=')[-1]
    atribuicao = atribuicao.rstrip(';')

    for nome, valor in identificadores.items():
        atribuicao = re.sub(rf'\b{nome}\b', str(valor), atribuicao)

    try:
        resultado = sympify(atribuicao)
        print(f"A atribuição está correta. Resultado: {resultado}")
    except SympifyError as e:
        print(f"A atribuição está incorreta. Erro: {e}")

def executar_expressao_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as arquivo:
            expressao = arquivo.read()

        estados, transicoes = criar_automato()

        if automato_atribuicao(expressao, estados, transicoes):
            avaliar_atribuicao(expressao)
        else:
            print("A expressão não segue o padrão definido pelo autômato.")

    except FileNotFoundError:
        print(f"O arquivo {nome_arquivo} não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Executando a expressão do arquivo "expressao.txt"
executar_expressao_arquivo("expressao.txt")
