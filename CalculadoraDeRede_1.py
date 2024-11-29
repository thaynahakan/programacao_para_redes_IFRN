'''1. Implemente uma calculadora de sub-rede em Python. O programa deve solicitar um endereço IP, uma
máscara de rede inicial e uma máscara de rede final. Para cada máscara de rede no intervalo
especificado, o programa deve calcular e exibir as seguintes informações:
a) Endereço de Rede
b) Primeiro Host
c) Último Host
d) Endereço de Broadcast
e) Máscara de Sub-rede em Decimal e Binário
f) Número de Hosts Válidos.
Requisitos:
a) NÃO utilize a biblioteca ipaddress;
b) Valide o endereço IP e as máscaras de rede fornecidas pelo usuário;
c) Salve os resultados em um arquivo no formato JSON (dicionário). Não subscreva arquivos
existentes;
d) Formate as saídas de forma clara e organizada (se quiser pode usar a biblioteca tabulate).'''

# Importação de bibliotecas necessárias
import json  # Para salvar os resultados em arquivos JSON
import os  # Para verificar a existência de arquivos no sistema
from tabulate import tabulate  # Para exibir dados formatados em tabela no console

# ===================== Funções Auxiliares =====================

def verificar_endereco_ip(endereco):
    """
    Valida o formato do endereço IP.
    - O endereço deve ser composto por quatro partes separadas por pontos.
    - Cada parte deve ser um número entre 0 e 255.
    """
    partes_endereco = endereco.split(".")
    if len(partes_endereco) != 4:
        raise ValueError("Formato de endereço IP inválido. Exemplo válido: '192.168.0.1'.")
    for segmento in partes_endereco:
        if not segmento.isdigit() or not (0 <= int(segmento) <= 255):
            raise ValueError("Formato de endereço IP inválido. Exemplo válido: '192.168.0.1'.")
    return endereco

def validar_prefixo_rede(prefixo):
    """
    Valida o prefixo da rede (máscara).
    - O prefixo deve ser um número entre 0 e 32.
    """
    if not (0 <= prefixo <= 32):
        raise ValueError("Prefixo de rede inválido. Deve estar entre 0 e 32.")
    return prefixo

def converter_ip_binario(endereco):
    """
    Converte o endereço IP para uma representação binária.
    - Cada segmento do endereço é convertido para 8 bits binários.
    """
    segmentos = map(int, endereco.split("."))
    return ''.join(f"{segmento:08b}" for segmento in segmentos)

def converter_binario_ip(binario):
    """
    Converte uma string binária em um endereço IP no formato decimal.
    - Divide a string em blocos de 8 bits e converte cada bloco em decimal.
    """
    segmentos = [str(int(binario[i:i+8], 2)) for i in range(0, 32, 8)]
    return ".".join(segmentos)

# ================= Funções de Negócio/Sub-redes ================

def gerar_informacoes_subrede(endereco, prefixo):
    """
    Gera informações detalhadas sobre uma sub-rede:
    - Calcula o endereço de rede, broadcast, primeiro e último host.
    - Calcula o total de hosts disponíveis.
    - Converte a máscara para os formatos binário e decimal.
    """
    # Converte o endereço IP para binário
    endereco_bin = converter_ip_binario(endereco)
    
    # Calcula a parte da rede (todos os bits adicionais são 0)
    rede_binaria = endereco_bin[:prefixo] + "0" * (32 - prefixo)
    
    # Calcula o endereço de broadcast (todos os bits adicionais são 1)
    broadcast_binaria = endereco_bin[:prefixo] + "1" * (32 - prefixo)
    
    # Calcula os endereços do primeiro e do último host
    primeiro_host = converter_binario_ip(rede_binaria[:-1] + "1")  # Muda o último bit para 1
    ultimo_host = converter_binario_ip(broadcast_binaria[:-1] + "0")  # Muda o último bit para 0
    
    # Calcula o número total de hosts válidos na sub-rede
    total_hosts = (2 ** (32 - prefixo)) - 2
    
    # Converte a máscara para os formatos binário e decimal
    mascara_binaria = "1" * prefixo + "0" * (32 - prefixo)
    mascara_decimal = converter_binario_ip(mascara_binaria)
    
    # Retorna as informações em um dicionário
    return {
        "CIDR": f"/{prefixo}",
        "Endereço da Rede": converter_binario_ip(rede_binaria),
        "Primeiro Host": primeiro_host,
        "Último Host": ultimo_host,
        "Broadcast": converter_binario_ip(broadcast_binaria),
        "Máscara de Rede": mascara_decimal,
        "Máscara Binária": mascara_binaria,
        "Total de Hosts": total_hosts
    }

def calcular_varias_subredes(endereco, prefixo_inicio, prefixo_fim):
    """
    Calcula informações para múltiplas sub-redes com base em um intervalo de prefixos.
    - Para cada prefixo no intervalo, calcula informações detalhadas da sub-rede.
    """
    lista_subredes = []
    for prefixo in range(prefixo_inicio, prefixo_fim + 1):
        lista_subredes.append(gerar_informacoes_subrede(endereco, prefixo))
    return lista_subredes

# ================== Funções de Entrada e Saída ==================

def salvar_em_json(dados, arquivo):
    """
    Salva os dados gerados em um arquivo JSON.
    - Verifica se o arquivo já existe para evitar sobrescrita.
    - Formata os dados de forma legível.
    """
    if os.path.exists(arquivo):
        raise FileExistsError(f"O arquivo '{arquivo}' já existe.")
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def mostrar_em_tabela(lista_dados):
    """
    Exibe as informações das sub-redes em formato de tabela.
    - Utiliza a biblioteca `tabulate` para formatar os dados.
    """
    linhas_tabela = []
    for subrede in lista_dados:
        linhas_tabela.append([
            subrede["CIDR"],
            subrede["Endereço da Rede"],
            subrede["Primeiro Host"],
            subrede["Último Host"],
            subrede["Broadcast"],
            subrede["Máscara de Rede"],
            subrede["Máscara Binária"],
            subrede["Total de Hosts"]
        ])
    
    cabecalhos = ["CIDR", "Endereço da Rede", "Primeiro Host", "Último Host", "Broadcast", 
                  "Máscara de Rede", "Máscara Binária", "Total de Hosts"]
    
    print(tabulate(linhas_tabela, headers=cabecalhos, tablefmt="grid"))

# ===================== Fluxo Principal ======================

def programa_principal():
    """
       Fluxo principal do programa.
    - Solicita informações ao usuário.
    - Calcula as sub-redes com base no intervalo de prefixos fornecido.
    - Salva os resultados em um arquivo JSON.
    - Exibe os resultados em formato de tabela.
    """
    while True:
        try:
            # Entrada do endereço IP
            while True:
                try:
                    endereco = input("Insira o endereço IP: ")
                    endereco = verificar_endereco_ip(endereco)
                    break
                except ValueError as erro_ip:
                    print(erro_ip)
            
            # Entrada do prefixo inicial
            while True:
                try:
                    prefixo_inicio = int(input("Insira o prefixo inicial (0-32): "))
                    prefixo_inicio = validar_prefixo_rede(prefixo_inicio)
                    break
                except ValueError as erro_prefixo:
                    print(erro_prefixo)
            
            # Entrada do prefixo final
            while True:
                try:
                    prefixo_fim = int(input("Insira o prefixo final (0-32): "))
                    prefixo_fim = validar_prefixo_rede(prefixo_fim)
                    if prefixo_inicio > prefixo_fim:
                        raise ValueError("O prefixo inicial deve ser menor ou igual ao final.")
                    break
                except ValueError as erro_prefixo:
                    print(erro_prefixo)
            
            # Cálculo das sub-redes no intervalo de prefixos
            subredes = calcular_varias_subredes(endereco, prefixo_inicio, prefixo_fim)
            
            # Salva os resultados em um arquivo JSON
            while True:
                try:
                    nome_arquivo = input("Digite o nome do arquivo para salvar (sem extensão): ") + ".json"
                    salvar_em_json(subredes, nome_arquivo)
                    print(f"Resultados salvos no arquivo {nome_arquivo}.")
                    break
                except FileExistsError as erro_arquivo:
                    print(erro_arquivo)
            
            # Exibe os resultados em formato de tabela
            mostrar_em_tabela(subredes)
            break  # Encerra o programa quando tudo for concluído com sucesso
        
        except Exception as erro_inesperado:
            print(f"Ocorreu um erro inesperado: {erro_inesperado}")

# ===================== Inicialização do Programa ======================

if __name__ == "__main__":
    programa_principal()
