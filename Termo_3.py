''' Desenvolver um programa que simula o site https://term.ooo/, mas com a palavra do dia sendo sorteada
a partir de um arquivo texto. A seguir tem o detalhamento das funcionalidades:
• Leitura do Arquivo:
o O programa deve ler um arquivo texto com uma lista de palavras.
o Cada linha do arquivo deve conter uma palavra com no mínimo 5 e no máximo 8 letras.
o O programa deve armazenar as palavras em uma lista.
• Sorteio da Palavra:
o O programa deve sortear uma palavra aleatória da lista de palavras.
o O programa informa quantas letras a palavra sorteada tem.
• Jogo:
o O usuário tem 6 tentativas para adivinhar a palavra sorteada;
o O usuário deve digitar uma palavra limitada a quantidade de letras que a palavra sorteada
possui (tratar caso a quantidade de letras seja diferente);
o Se a palavra for válida (possuir a mesma quantidade de caracteres da palavra sorteada), o
programa deve fornecer feedback sobre a tentativa:
▪ Para cada letra:
✓ Se a letra estiver na posição correta, a cor da letra deve ficar verde.
✓ Se a letra estiver presente na palavra, mas em posição incorreta, a cor da letra deve
ficar amarela.
✓ Se a letra não estiver presente na palavra, a cor da letra deve ficar cinza.
o O usuário pode tentar adivinhar a palavra novamente após cada tentativa.
• Vitória ou Derrota:
o Se o usuário adivinhar a palavra em 6 tentativas ou menos, o programa deve parabenizá-lo e
mostrar o número de tentativas utilizadas.
o Se o usuário não conseguir adivinhar a palavra em 6 tentativas, o programa deve revelar a
palavra e informar que o usuário perdeu.
'''

import random

def main():
    """
    Função principal que coordena a execução do programa.
    """
    # Nome do arquivo contendo as palavras
    nome_arquivo_palavras = "palavras.txt"

    # Carrega as palavras do arquivo
    palavras_disponiveis = carregar_palavras(nome_arquivo_palavras)
    if not palavras_disponiveis:
        print("Erro: Nenhuma palavra válida foi encontrada no arquivo.")
        return

    # Seleciona uma palavra aleatória e inicia o jogo
    palavra_sorteada = selecionar_palavra_aleatoria(palavras_disponiveis)
    executar_jogo(palavra_sorteada)

def carregar_palavras(nome_arquivo):
    """
    Carrega palavras de um arquivo de texto, filtrando aquelas com 5 a 8 letras.
    
    Args:
        nome_arquivo (str): Caminho para o arquivo contendo as palavras.
    
    Returns:
        list: Lista de palavras válidas.
    """
    try:
        with open(nome_arquivo, 'r') as arquivo:
            palavras_validas = [
                linha.strip().lower() 
                for linha in arquivo 
                if 5 <= len(linha.strip()) <= 8
            ]
    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
        return []
    return palavras_validas

def selecionar_palavra_aleatoria(lista_palavras):
    """
    Seleciona uma palavra aleatória da lista fornecida e informa sua quantidade de letras.
    
    Args:
        lista_palavras (list): Lista de palavras disponíveis para sorteio.
    
    Returns:
        str: Palavra sorteada.
    """
    palavra_selecionada = random.choice(lista_palavras)
    print(f"A palavra sorteada tem {len(palavra_selecionada)} letras.")
    return palavra_selecionada

def executar_jogo(palavra_escolhida):
    """
    Gerencia o jogo, permitindo ao jogador fazer tentativas até acertar ou esgotar as chances.
    
    Args:
        palavra_escolhida (str): Palavra que o jogador deve adivinhar.
    """
    tentativas_restantes = 6

    while tentativas_restantes > 0:
        print(f"\nTentativas restantes: {tentativas_restantes}")
        tentativa = input("Digite sua palavra: ").strip().lower()

        # Verifica se a tentativa possui o número correto de letras
        if len(tentativa) != len(palavra_escolhida):
            print(f"Erro: A palavra deve conter exatamente {len(palavra_escolhida)} letras.")
            continue

        # Verifica se o jogador acertou a palavra
        if tentativa == palavra_escolhida:
            print(f"Parabéns! Você acertou a palavra '{palavra_escolhida}' em {6 - tentativas_restantes + 1} tentativa(s)!")
            return

        # Fornece feedback sobre a tentativa
        print(f"Feedback: {avaliar_tentativa(palavra_escolhida, tentativa)}")

        # Reduz o número de tentativas restantes
        tentativas_restantes -= 1

    # Se o jogador não acertar em 6 tentativas
    print(f"\nVocê perdeu! A palavra correta era: '{palavra_escolhida}'.")

def avaliar_tentativa(palavra_alvo, tentativa_usuario):
    """
    Avalia a tentativa do jogador e retorna um feedback indicando as posições corretas e incorretas.
    
    Args:
        palavra_alvo (str): Palavra correta que o jogador precisa adivinhar.
        tentativa_usuario (str): Palavra fornecida pelo jogador.
    
    Returns:
        str: Feedback com cores (verde, amarelo, cinza) para cada letra.
    """
    feedback = []
    for indice, letra in enumerate(tentativa_usuario):
        if letra == palavra_alvo[indice]:
            feedback.append(f"\033[92m{letra}\033[0m")  # Verde: posição correta
        elif letra in palavra_alvo:
            feedback.append(f"\033[93m{letra}\033[0m")  # Amarelo: presente, mas em posição errada
        else:
            feedback.append(f"\033[90m{letra}\033[0m")  # Cinza: letra ausente
    return " ".join(feedback)

if __name__ == "__main__":
    main()
