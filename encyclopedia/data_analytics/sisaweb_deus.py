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

def extrair_dados_pertinentes(municipio_nome, inicio, final):
    """
    Extrai e salva dados pertinentes para o município e intervalo de datas especificados.
    """
    municipios = get_municipios(municipio_nome)
    if not municipios:
        print(f"Erro ao recuperar municípios para o nome: {municipio_nome}.")
        return

    for municipio in municipios:
        municipio_id = municipio['id']
        nome_municipio = municipio['nome']
        dados_importantes = {}

        tipos_importantes = [5, 6, 7]
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

# Lista de municípios
municipios = {
    "municipios": [
        "adamantina",
        "adolfo",
        "aguai",
        "aguas da prata",
        "aguas de lindóia",
        "aguas de santa bárbara",
        "aguas de são pedro",
        "agudos",
        "alambari",
        "alfredo marcondes",
        "altair",
        "altinópolis",
        "alto alegre",
        "alumínio",
        "álvares florence",
        "álvares machado",
        "álvaro de carvalho",
        "alvinlândia",
        "americana",
        "américo brasiliense",
        "américo de campos",
        "amparo",
        "analândia",
        "andradina",
        "angatuba",
        "ankiara",
        "apiaí",
        "aracariguama",
        "aracatuba",
        "aracoiaba da serra",
        "aramina",
        "arandu",
        "arapeí",
        "arapongas",
        "araraquara",
        "araras",
        "arco-íris",
        "arealva",
        "areias",
        "areiópolis",
        "ariranha",
        "artur nogueira",
        "aruã",
        "arujá",
        "aspásia",
        "assis",
        "atibaia",
        "auriflama",
        "avaí",
        "avanhandava",
        "avelar",
        "barra bonita",
        "barra do chapéu",
        "barra do turvo",
        "bariri",
        "barra de são francisco",
        "barretos",
        "bastos",
        "batatais",
        "bauru",
        "bebedouro",
        "bento de abreu",
        "bernardino de campos",
        "bertioga",
        "bilac",
        "birigui",
        "biritiba-mirim",
        "boa esperança do sul",
        "bocaina",
        "boituva",
        "bom jesus dos perdões",
        "bom sucesso de itararé",
        "borá",
        "boracéia",
        "borebi",
        "botucatu",
        "bragança paulista",
        "braúna",
        "brejo alegre",
        "brodowski",
        "brotas",
        "buri",
        "buritama",
        "buritizal",
        "cabrália paulista",
        "cabreúva",
        "caçapava",
        "cachoeira paulista",
        "caconde",
        "cafelândia",
        "caiabu",
        "caieiras",
        "caiuá",
        "cajamar",
        "cajati",
        "cajobi",
        "cajuru",
        "campina do monte alegre",
        "campinas",
        "campo limpo paulista",
        "campos do jordão",
        "campos novos paulista",
        "cananéia",
        "canas",
        "cândido mota",
        "cândido rodrigues",
        "canitar",
        "capão bonito",
        "capela do alto",
        "capivari",
        "caraguatatuba",
        "carapicuíba",
        "cardoso",
        "casabranca",
        "catanduva",
        "catiguá",
        "cedral",
        "cerqueira césar",
        "cerquilho",
        "cesário lange",
        "charqueada",
        "chavantes",
        "clementina",
        "colina",
        "colômbia",
        "conchal",
        "conchas",
        "coroados",
        "coronel macedo",
        "corumbataí",
        "cosmópolis",
        "cosmorama",
        "cotia",
        "cravinhos",
        "cristais paulista",
        "cruzália",
        "cruzeiro",
        "cubatão",
        "cunha",
        "descalvado",
        "diadema",
        "dirce reis",
        "divinolândia",
        "dobrada",
        "dois córregos",
        "dolcinópolis",
        "dourado",
        "dracena",
        "duartina",
        "dumont",
        "echaporã",
        "eldorado",
        "elias fausto",
        "elisiário",
        "embaúba",
        "embu das artes",
        "embu-guaçu",
        "emilianópolis",
        "engenheiro coelho",
        "espírito santo do pinhal",
        "espírito santo do turvo",
        "estiva gerbi",
        "estrela do norte",
        "euclides da cunha paulista",
        "fartura",
        "fernandópolis",
        "ferraz de vasconcelos",
        "florínia",
        "flórida paulista",
        "florínea",
        "franca",
        "francisco morato",
        "franco da rocha",
        "gabriel monteiro",
        "gália",
        "garça",
        "gastão vidigal",
        "gaviao peixoto",
        "general salgado",
        "getulina",
        "glicério",
        "guaimbê",
        "guaira",
        "guapiara",
        "guará",
        "guaraçaí",
        "guaraci",
        "guarani d'oeste",
        "guarantã",
        "guararapes",
        "guararema",
        "guaratinguetá",
        "guareí",
        "guariba",
        "guarujá",
        "guarulhos",
        "guatapará",
        "gusolândia",
        "herculândia",
        "holambra",
        "hortolândia",
        "iapu",
        "ibiúna",
        "ibiraci",
        "ibitinga",
        "ibitirama",
        "icém",
        "igaratá",
        "igaraçu do tietê",
        "igaraí",
        "ilhabela",
        "ilhabela",
        "imbirama",
        "inúbia paulista",
        "ipauçu",
        "ipiguá",
        "iporanga",
        "ipupiara",
        "iquitaia",
        "iquique",
        "irati",
        "itaberá",
        "itacolomi",
        "itaí",
        "itajobi",
        "itajubá",
        "itajurama",
        "itanhaém",
        "itaóca",
        "itapecerica da serra",
        "itapetininga",
        "itapeva",
        "itapevi",
        "itapira",
        "itapirapuã paulista",
        "itapolis",
        "itaquaquecetuba",
        "itararé",
        "itatiba",
        "itatui",
        "itauçu",
        "itaúba",
        "itáutinga",
        "itaí",
        "itu",
        "ituan",
        "itubera",
        "ituiutaba",
        "itupeva",
        "iturama",
        "jaboticabal",
        "jaci",
        "jacupiranga",
        "jaguariúna",
        "jales",
        "jandira",
        "jardinópolis",
        "jarinu",
        "jatobá",
        "jaú",
        "jeriquara",
        "joanópolis",
        "joão ramalho",
        "jose bonifácio",
        "júlio mesquita",
        "jundiaí",
        "junqueirópolis",
        "juquiá",
        "juquitiba",
        "lagoinha",
        "laranjal paulista",
        "lavínia",
        "lavrinhas",
        "leme",
        "lençóis paulista",
        "limeira",
        "lindóia",
        "lins",
        "lorena",
        "louveira",
        "lucélia",
        "lucianópolis",
        "luís antônio",
        "luzia",
        "macatuba",
        "macaubal",
        "maciário",
        "macuco",
        "madrid",
        "mairinque",
        "mamis"
    ]
}

# Itera sobre a lista de municípios e extrai os dados
for municipio in municipios['municipios']:
    extrair_dados_pertinentes(municipio, data_inicio, data_final)

print("Extração finalizada.")
