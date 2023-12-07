import re
from sympy import symbols, sympify

def automato_atribuicao(expressao):
    estados = {
        'q0': 0,  # Estado inicial
        'q1': 1,  # Identificador
        'q2': 2,  # Operador de atribuição '='
        'q3': 3,  # Número
        'q4': 4,  # Operador aritmético
        'q5': 5   # Estado final
    }

    transicoes = {
        0: {'letra': 1},
        1: {'letra': 1, 'digito': 1, '_': 1, 'espaco': 2},
        2: {'=': 3},
        3: {'digito': 4, 'letra': 4},
        4: {'digito': 4, 'letra': 4, 'op_arit': 4, 'pv': 5, 'espaco': 5},
        5: {'espaco': 5},
    }

    estado_atual = estados['q0']

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
            categoria = ' '
        else:
            raise ValueError(f"Caractere inválido na expressão: {char}")

        if categoria not in transicoes[estado_atual]:
            raise ValueError(f"Transição inválida do estado {estado_atual} com o caractere {char}")

        estado_atual = transicoes[estado_atual][categoria]

    return estado_atual == estados['q5']


def avaliar_atribuicao(expressao):
    linhas = expressao.split('\n')

    identificadores = {}
    for linha in linhas[:-2]:
        nome, valor = linha.split('=')
        identificadores[nome.strip()] = float(valor)

    atribuicao = linhas[-2]

    for nome, valor in identificadores.items():
        atribuicao = re.sub(rf'\b{nome}\b', str(valor), atribuicao)

    try:
        # Usar sympify para avaliar a expressão
        resultado = sympify(atribuicao)

        print(f"A atribuição está correta. Resultado: {resultado}")
    except Exception as e:
        print(f"A atribuição está incorreta. Erro: {e}")


# Exemplo de uso:
expressao_exemplo = """bola = 10
x = 5
casa = 2

bola=32+x*casa;"""

avaliar_atribuicao(expressao_exemplo)