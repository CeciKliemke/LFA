import os
import re

def ler_arquivo(caminho):
    with open(caminho, 'r') as arquivo:
        return arquivo.read()
def automato_atribuicao(expressao):
    # Definindo estados
    estados = {
        'q0': 0,  # Estado inicial
        'q1': 1,  # Identificador
        'q2': 2,  # Operador de atribuição '='
        'q3': 3,  # Número
        'q4': 4,  # Operador aritmético
        'q5': 5   # Estado final
    }

    # Definindo transições
    transicoes = {
        0: {'letra': 1},
        1: {'letra': 1, 'digito': 1, '_': 1, 'espaco': 2},
        2: {'=': 3},
        3: {'digito': 4, 'letra': 4},
        4: {'digito': 4, 'letra': 4, 'op_arit': 4, 'pv': 5, 'espaco': 5},
    }

    # Inicializando estado atual
    estado_atual = estados['q0']

    # Processando a expressão caractere por caractere
    for char in expressao:
        if char.isalpha():
            categoria = 'letra'
        elif char.isdigit():
            categoria = 'digito'
        elif char == '_':
            categoria = '_'
        elif char == '=':
            categoria = '='
        elif char in ('+', '-', '*', '/'):
            categoria = 'op_arit'
        elif char == ';':
            categoria = 'pv'
        elif char.isspace():
            categoria = 'espaco'
        else:
            raise ValueError(f"Caractere inválido na expressão: {char}")

        # Verificando transições
        if categoria not in transicoes[estado_atual]:
            raise ValueError(f"Transição inválida do estado {estado_atual} com o caractere {char}")

        estado_atual = transicoes[estado_atual][categoria]

    # Verificando se o estado final foi alcançado
    return estado_atual == estados['q5']

def avaliar_atribuicao(expressao):
    # Separando a expressão em linhas
    linhas = expressao.split('\n')

    # Processando as linhas iniciais para definir os valores dos identificadores
    identificadores = {}
    for linha in linhas[:-2]:
        nome, valor = linha.split('=')
        identificadores[nome.strip()] = float(valor)

    # Avaliando a expressão de atribuição
    atribuicao = linhas[-2]
    if automato_atribuicao(atribuicao):
        # Substituindo os identificadores pelos valores
        for nome, valor in identificadores.items():
            atribuicao = re.sub(rf'\b{nome}\b', str(valor), atribuicao)

        # Avaliando a expressão e imprimindo o resultado
        resultado = eval(atribuicao)
        print(f"A atribuição está correta. Resultado: {resultado}")
    else:
        print("A atribuição está incorreta.")

# Obtém o caminho do diretório atual
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Constrói o caminho completo para o arquivo de texto
caminho_arquivo = os.path.join(diretorio_atual, 'teste.txt')

# Lê o conteúdo do arquivo
expressao_do_arquivo = ler_arquivo(caminho_arquivo)

# Avalia a atribuição
avaliar_atribuicao(expressao_do_arquivo)