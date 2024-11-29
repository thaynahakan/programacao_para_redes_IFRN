'''A dificuldade de minerar bitcoins envolve ocorre porque é necessário executar o que se chama de prova
de trabalho. Em outras palavras, vários mineradores competem para realizar uma tarefa; aquele que
primeiro realizar é o minerador campeão da atividade e recebe uma boa recompensa. Na prática, a
atividade a realizar é: receber um conjunto de transações (um conjunto de bytes) e calcular o hash SHA256 deles, mas tem um detalhe: um número de quatro bytes deve ser adicionado no início dos bytes
recebidos (chame-o de nonce) e dos 256 bits de resultado uma determinada quantidade inicial deve ser
zero. O minerador que descobrir o nonce certo é o vencedor. Graficamente:
Portanto, minerar é: a) escolher um nonce; b) juntar com os bytes da entrada; c) calcular o hash desse
conjunto; d) verificar se o hash resultante inicia com uma certa quantidade de bits em zero; e) se o hash
calculado não atende ao requisito, repetir o processo.
Faça uma função em Python de nome findNonce que recebe três argumentos:
• dataToHash – um conjunto de bytes
• bitsToBeZero – o número de bits iniciais que deve ser zero no hash
e devolve:
• o nonce encontrado
• o tempo (em segundos) que demorou para encontrar o nonce
Ao final, faça um programa que usa a função para preencher a seguinte tabela:
Texto a validarpython minerar.py
(converta para bytes antes de chamar) Bits em zero Nonce Tempo (em s)
“Esse é fácil” 8
“Esse é fácil” 10
“Esse é fácil” 15
“Texto maior muda o tempo?” 8
“Texto maior muda o tempo?” 10
“Texto maior muda o tempo?” 15
“É possível calcular esse?” 18
“É possível calcular esse?” 19
“É possível calcular esse?” 20
Sua resposta deve ser 3 arquivos: um arquivo com o programa principal, um segundo com a função e
outras auxiliares, se necessário e o terceiro com a tabela preenchida (em formato doc, PDF ou txt).'''

import hashlib
import time

def localizar_nonce(entrada_dados: bytes, bits_necessarios_zero: int):
    """
    Função para encontrar um nonce que resulta em um hash com os bits iniciais sendo zero.
    
    Args:
        entrada_dados (bytes): Dados de entrada para o cálculo do hash.
        bits_necessarios_zero (int): Número de bits iniciais que devem ser zero no hash.

    Returns:
        int: O nonce que satisfaz a condição.
        float: O tempo, em segundos, necessário para encontrar o nonce.
    """
    contador_nonce = 0
    inicio_tempo = time.time()
    
    while True:
        # Combinar o nonce com os dados fornecidos
        dados_nonce = contador_nonce.to_bytes(4, byteorder='little')
        dados_completos = dados_nonce + entrada_dados
        
        # Calcular o hash SHA256
        hash_gerado = hashlib.sha256(dados_completos).digest()
        
        # Converter o hash em bits
        hash_em_bits = ''.join(f'{byte:08b}' for byte in hash_gerado)
        
        # Verificar se os bits iniciais são zeros
        if hash_em_bits.startswith('0' * bits_necessarios_zero):
            tempo_total = time.time() - inicio_tempo
            return contador_nonce, tempo_total
        
        # Incrementar o nonce
        contador_nonce += 1

# Lista de textos para teste e quantidade de bits em zero
textos_para_testar = [
    "Esse é fácil", "Esse é fácil", "Esse é fácil", 
    "Texto maior muda o tempo?", "Texto maior muda o tempo?", "Texto maior muda o tempo?", 
    "É possível calcular esse?", "É possível calcular esse?", "É possível calcular esse?"
]
quantidade_bits_zero = [8, 10, 15, 8, 10, 15, 18, 19, 20]

# Tabela para armazenar os resultados
tabela_resultados = []

for texto, bits_zero in zip(textos_para_testar, quantidade_bits_zero):
    dados_em_bytes = texto.encode('utf-8')
    nonce_encontrado, tempo_decorrido = localizar_nonce(dados_em_bytes, bits_zero)
    tabela_resultados.append((texto, bits_zero, nonce_encontrado, tempo_decorrido))

# Exibir os resultados em formato de tabela
print(f"{'Texto':<30} {'Bits em Zero':<15} {'Nonce':<15} {'Tempo (s)':<15}")
for resultado in tabela_resultados:
    print(f"{resultado[0]:<30} {resultado[1]:<15} {resultado[2]:<15} {resultado[3]:<15.4f}")
