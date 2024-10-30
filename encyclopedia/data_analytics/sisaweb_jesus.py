import requests
import json
import pandas as pd
import os
import re
from datetime import datetime

# URL base da API
BASE_URL = "https://vigent.saude.sp.gov.br/sisaweb_api/"

def sanitize_filename(nome):
    """
    Sanitiza o nome do arquivo, removendo ou substituindo caracteres especiais.
    """
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', nome)

def get_municipios(nome=""):
    """
    Obtém a lista de municípios correspondentes ao nome fornecido.
    """
    try:
        response = requests.get(f"{BASE_URL}lista.php?nome={nome}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter municípios: {e}")
        return None

def get_dados(tipo, municipio_id, inicio, final):
    """
    Obtém dados específicos para um município, tipo e intervalo de datas.
    """
    try:
        url = f"{BASE_URL}dados.php?tipo={tipo}&id={municipio_id}&inicio={inicio}&final={final}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter dados para o município ID {municipio_id}: {e}")
        return None

def salvar_csv(dados, nome_arquivo):
    """
    Salva os dados fornecidos em um arquivo CSV com o nome especificado.
    """
    if dados:
        df = pd.DataFrame(dados)
        df.to_csv(nome_arquivo, index=False)
        print(f"Arquivo CSV '{nome_arquivo}' criado com sucesso.")

def extrair_dados_municipio(municipio_nome, inicio, final):
    """
    Extrai e salva dados pertinentes para o município e intervalo de datas especificados.
    """
    municipios = get_municipios(municipio_nome)
    if not municipios:
        print(f"Erro ao recuperar municípios para o nome: {municipio_nome}.")
        return

    # Encontra o município que corresponde exatamente ao nome fornecido
    municipio = next((m for m in municipios if m['nome'].lower() == municipio_nome.lower()), None)
    if not municipio:
        print(f"Município '{municipio_nome}' não encontrado.")
        return

    municipio_id = municipio['id']
    nome_municipio = municipio['nome']
    dados_importantes = {}

    tipos_importantes = [11, 13]
    for tipo in tipos_importantes:
        dados = get_dados(tipo, municipio_id, inicio, final)
        if dados:
            nome_arquivo = f"{sanitize_filename(nome_municipio)}_tipo_{tipo}_dados.csv"
            salvar_csv(dados, nome_arquivo)
            dados_importantes[tipo] = dados

    print(f"Dados extraídos para o município: {nome_municipio}")

# Definir intervalo de datas válido
data_inicio = "2023-01-01"
data_final = datetime.today().strftime('%Y-%m-%d')

# Especifique o município desejado
municipio_desejado = "sao jose do rio preto"

# Extrai os dados para o município especificado
extrair_dados_municipio(municipio_desejado, data_inicio, data_final)

print("Extração finalizada.")
