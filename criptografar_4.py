import os
import sys

def criptografar_xor(arquivo_origem, senha, arquivo_destino):
    """
    Criptografa os bytes de um arquivo usando a operação XOR com base em uma senha.

    Args:
        arquivo_origem (str): Caminho do arquivo de origem.
        senha (str): Palavra-passe para a operação XOR.
        arquivo_destino (str): Caminho do arquivo de destino.

    Returns:
        None
    """
    # Verifica se o arquivo de origem existe
    if not os.path.isfile(arquivo_origem):
        print(f"Erro: O arquivo de origem '{arquivo_origem}' não foi encontrado.")
        return
    
    # Verifica se o arquivo de destino já existe para evitar sobrescrita
    if os.path.exists(arquivo_destino):
        print(f"Erro: O arquivo de destino '{arquivo_destino}' já existe. Escolha outro nome para evitar sobrescrita.")
        return

    # Verifica se a senha está preenchida
    if not senha:
        print("Erro: A palavra-passe não pode ser vazia.")
        return

    try:
        # Abre o arquivo de origem em modo binário para leitura
        with open(arquivo_origem, 'rb') as origem:
            conteudo_origem = origem.read()
        
        # Prepara um array de bytes para armazenar os dados criptografados
        dados_criptografados = bytearray()
        tamanho_senha = len(senha)
        
        # Aplica a criptografia XOR
        for i, byte in enumerate(conteudo_origem):
            byte_criptografado = byte ^ ord(senha[i % tamanho_senha])
            dados_criptografados.append(byte_criptografado)
        
        # Grava os dados criptografados no arquivo de destino
        with open(arquivo_destino, 'wb') as destino:
            destino.write(dados_criptografados)

        print(f"Criptografia concluída! O arquivo foi salvo como '{arquivo_destino}'.")
    
    except IOError as erro_io:
        print(f"Erro de entrada/saída: {erro_io}")
    except Exception as erro_generico:
        print(f"Ocorreu um erro inesperado: {erro_generico}")

def main():
    """
    Função principal para coordenar a entrada e execução do programa.
    """
    # Confirma se os argumentos foram fornecidos corretamente
    if len(sys.argv) != 4:
        print("Uso correto: python programa.py <arquivo_origem> <palavra_passe> <arquivo_destino>")
        return

    # Obtém os argumentos da linha de comando
    caminho_arquivo_origem = sys.argv[1]
    senha = sys.argv[2]
    caminho_arquivo_destino = sys.argv[3]

    # Executa a criptografia XOR
    criptografar_xor(caminho_arquivo_origem, senha, caminho_arquivo_destino)

if __name__ == "__main__":
    main()
