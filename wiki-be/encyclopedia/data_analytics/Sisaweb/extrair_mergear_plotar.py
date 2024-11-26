# Importação das bibliotecas necessárias
import requests
import json
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import re
from datetime import datetime, timedelta
from shapely import wkt

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

    Parâmetros:
    - nome (str): Nome ou parte do nome do município.

    Retorna:
    - Lista de dicionários com informações dos municípios correspondentes.
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

    Parâmetros:
    - tipo (int): Tipo de dado a ser extraído.
    - municipio_id (int): ID do município.
    - inicio (str): Data de início no formato 'YYYY-MM-DD'.
    - final (str): Data de fim no formato 'YYYY-MM-DD'.

    Retorna:
    - Dados no formato JSON.
    """
    try:
        url = f"{BASE_URL}dados.php?tipo={tipo}&id={municipio_id}&inicio={inicio}&final={final}&censitario=1"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter dados para o município ID {municipio_id}: {e}")
        return None

def calcular_intervalo_semanas(semanas=3):
    """
    Calcula a data de início e de fim para o intervalo de semanas fornecido.

    Parâmetros:
    - semanas (int): Número de semanas anteriores a partir da data atual.

    Retorna:
    - Tuple contendo as datas de início e fim no formato 'YYYY-MM-DD'.
    """
    hoje = datetime.today()
    inicio = hoje - timedelta(weeks=semanas)
    return inicio.strftime('%Y-%m-%d'), hoje.strftime('%Y-%m-%d')

def extrair_dados_municipio(municipio_nome, semanas=3, tipos=[4]):
    """
    Extrai e retorna dados pertinentes para o município e intervalo de semanas especificados.

    Parâmetros:
    - municipio_nome (str): Nome do município.
    - semanas (int): Número de semanas anteriores a partir da data atual.
    - tipos (list): Lista de tipos de dados a serem extraídos.

    Retorna:
    - DataFrame concatenado com os dados extraídos.
    """
    inicio, final = calcular_intervalo_semanas(semanas)
    municipios = get_municipios(municipio_nome)
    if not municipios:
        print(f"Erro ao recuperar municípios para o nome: {municipio_nome}.")
        return None

    # Encontra o município que corresponde exatamente ao nome fornecido (case-insensitive)
    municipio = next((m for m in municipios if m['nome'].lower() == municipio_nome.lower()), None)
    if not municipio:
        print(f"Município '{municipio_nome}' não encontrado.")
        return None

    municipio_id = municipio['id']
    nome_municipio = municipio['nome']

    dados_frames = []

    for tipo in tipos:
        dados = get_dados(tipo, municipio_id, inicio, final)
        if dados:
            df = pd.DataFrame(dados)
            dados_frames.append(df)

    if dados_frames:
        df_concatenado = pd.concat(dados_frames, ignore_index=True)
        print(f"Dados extraídos para o município: {nome_municipio}, para as últimas {semanas} semanas.")
        return df_concatenado
    else:
        print("Nenhum dado foi extraído.")
        return None

def ler_dados_filtrados(caminho_csv):
    """
    Lê o arquivo CSV filtrado e o converte em um GeoDataFrame, assumindo que a coluna 'geometry' está em WKT.

    Parâmetros:
    - caminho_csv (str): Caminho para o arquivo CSV filtrado.

    Retorna:
    - GeoDataFrame com os dados carregados.
    """
    try:
        df = pd.read_csv(caminho_csv)
        if 'geometry' in df.columns:
            # Converte a coluna 'geometry' de WKT para objetos geométricos
            df['geometry'] = df['geometry'].apply(wkt.loads)
            gdf = gpd.GeoDataFrame(df, geometry='geometry')
            print("Dados filtrados carregados com sucesso como GeoDataFrame!")
            return gdf
        else:
            print("A coluna 'geometry' não está presente no CSV.")
            return None
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV filtrado: {e}")
        return None

def realizar_merge(gdf_geo, df_dados, chave_geo='CD_SETOR', chave_dados='censitario'):
    """
    Realiza o merge entre o GeoDataFrame e o DataFrame de dados, mantendo todas as linhas do GeoDataFrame.

    Parâmetros:
    - gdf_geo (GeoDataFrame): GeoDataFrame com os dados geoespaciais.
    - df_dados (DataFrame): DataFrame com os dados a serem combinados.
    - chave_geo (str): Nome da coluna chave no GeoDataFrame.
    - chave_dados (str): Nome da coluna chave no DataFrame de dados.

    Retorna:
    - GeoDataFrame resultante do merge.
    """
    df_dados = df_dados.copy()
    if chave_dados in df_dados.columns:
        df_dados[chave_dados] = df_dados[chave_dados].astype(str)

    if chave_geo in gdf_geo.columns:
        gdf_geo[chave_geo] = gdf_geo[chave_geo].astype(str)

    gdf_merged = gdf_geo.merge(df_dados, how='left', left_on=chave_geo, right_on=chave_dados)
    print("Merge realizado com sucesso. Todas as linhas do GeoDataFrame foram mantidas.")
    return gdf_merged

def calcular_metricas(gdf):
    """
    Calcula as métricas necessárias para a análise e adiciona colunas ao GeoDataFrame.

    Parâmetros:
    - gdf (GeoDataFrame): GeoDataFrame com os dados combinados.

    Retorna:
    - GeoDataFrame com as métricas calculadas.
    """
    # Converte colunas relevantes para numérico, tratando erros
    colunas_numericas = ['trabalhados', 'nao_trabalhados', 'im_aegypti']
    for coluna in colunas_numericas:
        if coluna in gdf.columns:
            gdf[coluna] = pd.to_numeric(gdf[coluna], errors='coerce').fillna(0)

    # Métrica de tratamento de imóveis (imóveis trabalhados)
    gdf['tratamento_imoveis'] = gdf.apply(
        lambda row: row['trabalhados'] / (row['trabalhados'] + row['nao_trabalhados'])
        if (row['trabalhados'] + row['nao_trabalhados']) > 0 else 0,
        axis=1
    )

    # Métrica de imóveis não trabalhados
    gdf['nao_trabalhados_ratio'] = gdf.apply(
        lambda row: row['nao_trabalhados'] / (row['trabalhados'] + row['nao_trabalhados'])
        if (row['trabalhados'] + row['nao_trabalhados']) > 0 else 0,
        axis=1
    )

    # Incidência de Aedes aegypti por 1000 imóveis trabalhados
    gdf['incidencia_aedes'] = gdf.apply(
        lambda row: (row['im_aegypti'] / row['trabalhados']) * 1000
        if row['trabalhados'] > 0 else 0,
        axis=1
    )

    print("Métricas calculadas com sucesso.")
    return gdf

def criar_mapas(gdf):
    """
    Gera mapas de calor com base nas métricas calculadas.

    Parâmetros:
    - gdf (GeoDataFrame): GeoDataFrame com as métricas calculadas.

    Retorna:
    - None
    """
    # Define o sistema de referência de coordenadas (CRS)
    gdf.crs = "EPSG:4326"

    # Mapa de calor para imóveis não trabalhados
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    gdf.plot(column='nao_trabalhados_ratio', ax=ax, legend=True, cmap='Blues', edgecolor='black')
    ax.set_title('Proporção de Imóveis Não Trabalhados (Dados de 3 Semanas)')
    plt.show()

    # Mapa de calor para incidência de Aedes aegypti
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    gdf.plot(column='incidencia_aedes', ax=ax, legend=True, cmap='Reds', edgecolor='black')
    ax.set_title('Incidência de Aedes aegypti por 1000 Imóveis Trabalhados (Dados de 3 Semanas)')
    plt.show()

    # Mapa de calor para tratamento de imóveis (imóveis trabalhados)
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    gdf.plot(column='tratamento_imoveis', ax=ax, legend=True, cmap='OrRd', edgecolor='black')
    ax.set_title('Proporção de Imóveis Trabalhados (Dados de 3 Semanas)')
    plt.show()

def salvar_geodataframe_csv(gdf, caminho_csv):
    """
    Salva o GeoDataFrame em um arquivo CSV, convertendo a coluna 'geometry' para WKT.

    Parâmetros:
    - gdf (GeoDataFrame): GeoDataFrame a ser salvo.
    - caminho_csv (str): Caminho para o arquivo CSV de saída.

    Retorna:
    - None
    """
    try:
        gdf = gdf.copy()
        gdf['geometry'] = gdf['geometry'].apply(lambda geom: geom.wkt if geom else None)
        gdf.to_csv(caminho_csv, index=False)
        print(f"GeoDataFrame salvo com sucesso em CSV: {caminho_csv}")
    except Exception as e:
        print(f"Erro ao salvar o GeoDataFrame em CSV: {e}")

# Configurações iniciais
municipio_desejado = "SAO JOSE DO RIO PRETO"
semanas_para_extrair = 3
tipos_de_dados = [4]  # Tipo 4, conforme necessário
caminho_dados_filtrados = "dados_filtrados.csv"  # Caminho para o arquivo CSV filtrado
caminho_para_salvar = "dados_merged.csv"  # Caminho para salvar o GeoDataFrame combinado

# Fluxo principal
if __name__ == "__main__":
    # Etapa 1: Extrair os dados do município
    df_dados = extrair_dados_municipio(municipio_desejado, semanas=semanas_para_extrair, tipos=tipos_de_dados)
    if df_dados is not None:
        # Etapa 2: Ler o arquivo filtrado como GeoDataFrame
        gdf_filtrado = ler_dados_filtrados(caminho_dados_filtrados)
        if gdf_filtrado is not None:
            # Etapa 3: Realizar o merge dos dados
            gdf_merged = realizar_merge(gdf_filtrado, df_dados)
            # Etapa 4: Calcular as métricas necessárias
            gdf_metricas = calcular_metricas(gdf_merged)
            # Etapa 5: Salvar o GeoDataFrame combinado e com métricas em CSV
            salvar_geodataframe_csv(gdf_metricas, caminho_para_salvar)
            # Etapa 6: Criar os mapas de calor
            criar_mapas(gdf_metricas)
