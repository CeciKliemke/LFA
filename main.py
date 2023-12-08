import re
from sympy import sympify, SympifyError

def criar_automato():
    """Cria e retorna o autômato finito determinístico."""
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
        2: {'espaco': 2, '=': 3},
        3: {'digito': 4, 'letra': 4, 'espaco': 3},
        4: {'digito': 4, 'letra': 4, 'op_arit': 4, 'pv': 5, 'espaco': 5},
        5: {'espaco': 5},
    }

    return estados, transicoes

def automato_atribuicao(expressao, estados, transicoes):
    """Verifica se a expressão segue o padrão definido pelo autômato."""
    estado_atual = estados['q0']

    for char in expressao:
        if estado_atual == estados['q5']:
            break  # Sai do loop se o estado final for alcançado

        categoria = obter_categoria(char)

        if estado_atual not in transicoes or categoria not in transicoes[estado_atual]:
            print(f"DEBUG: Estado atual: {estado_atual}, Categoria: {categoria}, Caractere: {char}")
            raise ValueError(f"Transição inválida do estado {estado_atual} com o caractere {char}")

        estado_atual = transicoes[estado_atual][categoria]

    return estado_atual == estados['q5']



def obter_categoria(char):
    """Obtém a categoria do caractere."""
    if char.isalpha():
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
    """Avalia a atribuição e imprime o resultado."""
    linhas = expressao.split('\n')

    identificadores = {}
    for linha in linhas[:-1]:  # Processa todas as linhas, exceto a última
        if '=' in linha:
            nome, valor = linha.split('=')
            identificadores[nome.strip()] = float(valor.strip())

    # A última linha é a expressão a ser avaliada
    atribuicao = linhas[-1].split('=')[-1]  # Pega apenas a expressão após o '='
    atribuicao = atribuicao.rstrip(';')  # Remove o ponto e vírgula final

    # Substitui os identificadores na expressão pela sua respectiva atribuição
    for nome, valor in identificadores.items():
        atribuicao = re.sub(rf'\b{nome}\b', str(valor), atribuicao)

    try:
        resultado = sympify(atribuicao)
        print(f"A atribuição está correta. Resultado: {resultado}")
    except SympifyError as e:
        print(f"A atribuição está incorreta. Erro: {e}")


# Exemplo de uso:
expressao_exemplo = """cubo = 6
triangulo = 3
pentagono = 5
arminha = 17

petangono=14+triangulo/3-cubo+arminha;"""

# Criar o autômato
estados, transicoes = criar_automato()

# Verificar se a expressão segue o padrão do autômato
if automato_atribuicao(expressao_exemplo, estados, transicoes):
    avaliar_atribuicao(expressao_exemplo)
else:
    print("A expressão não segue o padrão definido pelo autômato.")