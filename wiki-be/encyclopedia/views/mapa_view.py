import os
import requests
import pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend suitable for server environments
import matplotlib.pyplot as plt
import re
from datetime import datetime, timedelta
from shapely import wkt
from django.http import HttpResponse, HttpResponseServerError
from django.conf import settings
import logging
from rest_framework.decorators import api_view

# Configure logging
logger = logging.getLogger(__name__)

# URL base da API sisaweb
BASE_URL = "https://vigent.saude.sp.gov.br/sisaweb_api/"

def preparar_dados():
    """
    Prepara os dados necessários para gerar os mapas.

    Returns:
        gpd.GeoDataFrame: GeoDataFrame com as métricas calculadas.
        None: Se ocorrer um erro.
    """
    try:
        # Configurações
        municipio_desejado = "SAO JOSE DO RIO PRETO"
        semanas_para_extrair = 3
        tipos_de_dados = [4]  # Tipo 4, conforme necessário

        # Atualizar o caminho para 'dados_filtrados.csv' conforme a estrutura do seu projeto
        caminho_dados_filtrados = os.path.join(
            settings.BASE_DIR,
            'encyclopedia',
            'data_analytics',
            'Sisaweb',
            'dados_filtrados.csv'
        )

        # Etapa 1: Extrair dados do sisaweb
        df_dados = extrair_dados_municipio(municipio_desejado, semanas_para_extrair, tipos_de_dados)
        if df_dados is None:
            logger.error("Falha ao extrair dados do sisaweb.")
            return None

        # Etapa 2: Ler dados geoespaciais
        gdf_filtrado = ler_dados_filtrados(caminho_dados_filtrados)
        if gdf_filtrado is None:
            logger.error("Falha ao ler dados geoespaciais.")
            return None

        # Etapa 3: Realizar o merge dos dados
        gdf_merged = realizar_merge(gdf_filtrado, df_dados)
        if gdf_merged is None:
            logger.error("Falha ao realizar o merge dos dados.")
            return None

        # Etapa 4: Calcular métricas
        gdf_metricas = calcular_metricas(gdf_merged)
        return gdf_metricas

    except Exception as e:
        logger.exception("Ocorreu um erro ao preparar os dados.")
        return None

@api_view(['GET'])
def mapa_nao_trabalhados(request):
    """
    View para gerar e retornar o mapa de imóveis não trabalhados.
    """
    gdf = preparar_dados()
    if gdf is not None:
        try:
            # Gerar o mapa
            fig, ax = plt.subplots(1, 1, figsize=(12, 8))
            gdf.plot(column='nao_trabalhados_ratio', ax=ax, legend=True, cmap='Blues', edgecolor='black')
            ax.set_title('Proporção de Imóveis Não Trabalhados (Dados de 3 Semanas)')

            # Salvar o mapa em um buffer de memória
            from io import BytesIO
            buffer = BytesIO()
            fig.savefig(buffer, format='jpeg', bbox_inches='tight')
            plt.close(fig)
            buffer.seek(0)

            # Retornar o mapa como resposta HTTP
            return HttpResponse(buffer, content_type='image/jpeg')
        except Exception as e:
            logger.exception("Ocorreu um erro ao gerar o mapa.")
            return HttpResponseServerError("Erro ao gerar o mapa de imóveis não trabalhados.")
    else:
        return HttpResponseServerError("Erro ao preparar os dados para o mapa.")

@api_view(['GET'])
def mapa_incidencia_aedes(request):
    """
    View para gerar e retornar o mapa de incidência de Aedes aegypti.
    """
    gdf = preparar_dados()
    if gdf is not None:
        try:
            # Gerar o mapa
            fig, ax = plt.subplots(1, 1, figsize=(12, 8))
            gdf.plot(column='incidencia_aedes', ax=ax, legend=True, cmap='Reds', edgecolor='black')
            ax.set_title('Incidência de Aedes aegypti por 1000 Imóveis Trabalhados (Dados de 3 Semanas)')

            # Salvar o mapa em um buffer de memória
            from io import BytesIO
            buffer = BytesIO()
            fig.savefig(buffer, format='jpeg', bbox_inches='tight')
            plt.close(fig)
            buffer.seek(0)

            # Retornar o mapa como resposta HTTP
            return HttpResponse(buffer, content_type='image/jpeg')
        except Exception as e:
            logger.exception("Ocorreu um erro ao gerar o mapa.")
            return HttpResponseServerError("Erro ao gerar o mapa de incidência de Aedes aegypti.")
    else:
        return HttpResponseServerError("Erro ao preparar os dados para o mapa.")

@api_view(['GET'])
def mapa_tratamento_imoveis(request):
    """
    View para gerar e retornar o mapa de tratamento de imóveis.
    """
    gdf = preparar_dados()
    if gdf is not None:
        try:
            # Gerar o mapa
            fig, ax = plt.subplots(1, 1, figsize=(12, 8))
            gdf.plot(column='tratamento_imoveis', ax=ax, legend=True, cmap='OrRd', edgecolor='black')
            ax.set_title('Proporção de Imóveis Trabalhados (Dados de 3 Semanas)')

            # Salvar o mapa em um buffer de memória
            from io import BytesIO
            buffer = BytesIO()
            fig.savefig(buffer, format='jpeg', bbox_inches='tight')
            plt.close(fig)
            buffer.seek(0)

            # Retornar o mapa como resposta HTTP
            return HttpResponse(buffer, content_type='image/jpeg')
        except Exception as e:
            logger.exception("Ocorreu um erro ao gerar o mapa.")
            return HttpResponseServerError("Erro ao gerar o mapa de tratamento de imóveis.")
    else:
        return HttpResponseServerError("Erro ao preparar os dados para o mapa.")

# --- Funções Auxiliares ---

def get_municipios(nome=""):
    """
    Obtém a lista de municípios correspondentes ao nome fornecido a partir da API sisaweb.
    """
    try:
        response = requests.get(f"{BASE_URL}lista.php?nome={nome}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Erro ao buscar municípios: {e}")
        return None

def get_dados(tipo, municipio_id, inicio, final):
    """
    Obtém dados do tipo especificado para o município e intervalo de datas fornecidos.
    """
    try:
        url = f"{BASE_URL}dados.php?tipo={tipo}&id={municipio_id}&inicio={inicio}&final={final}&censitario=1"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Erro ao buscar dados para o município ID {municipio_id}: {e}")
        return None

def calcular_intervalo_semanas(semanas=3):
    """
    Calcula as datas de início e fim para o número de semanas fornecido a partir de hoje.
    """
    hoje = datetime.today()
    inicio = hoje - timedelta(weeks=semanas)
    return inicio.strftime('%Y-%m-%d'), hoje.strftime('%Y-%m-%d')

def extrair_dados_municipio(municipio_nome, semanas=3, tipos=[4]):
    """
    Extrai e retorna dados para o município e intervalo de datas especificados.
    """
    inicio, final = calcular_intervalo_semanas(semanas)
    municipios = get_municipios(municipio_nome)
    if not municipios:
        logger.error(f"Nenhum município encontrado com o nome: {municipio_nome}")
        return None

    municipio = next((m for m in municipios if m['nome'].lower() == municipio_nome.lower()), None)
    if not municipio:
        logger.error(f"Município '{municipio_nome}' não encontrado.")
        return None

    municipio_id = municipio['id']
    dados_frames = []

    for tipo in tipos:
        dados = get_dados(tipo, municipio_id, inicio, final)
        if dados:
            df = pd.DataFrame(dados)
            dados_frames.append(df)
        else:
            logger.warning(f"Nenhum dado retornado para o tipo {tipo}.")

    if dados_frames:
        df_concatenado = pd.concat(dados_frames, ignore_index=True)
        logger.info(f"Dados extraídos para o município ID {municipio_id}.")
        return df_concatenado
    else:
        logger.error("Nenhum dado para concatenar.")
        return None

def ler_dados_filtrados(caminho_csv):
    """
    Lê os dados filtrados do CSV e converte em um GeoDataFrame.
    """
    try:
        if not os.path.exists(caminho_csv):
            logger.error(f"O arquivo {caminho_csv} não foi encontrado.")
            return None

        df = pd.read_csv(caminho_csv)
        if 'geometry' in df.columns:
            df['geometry'] = df['geometry'].apply(wkt.loads)
            gdf = gpd.GeoDataFrame(df, geometry='geometry')
            logger.info("Dados geoespaciais carregados com sucesso.")
            return gdf
        else:
            logger.error("Coluna 'geometry' não encontrada no CSV.")
            return None
    except Exception as e:
        logger.error(f"Erro ao ler o arquivo CSV: {e}")
        return None

def realizar_merge(gdf_geo, df_dados, chave_geo='CD_SETOR', chave_dados='censitario'):
    """
    Realiza o merge dos dados geoespaciais com os dados do sisaweb nas chaves especificadas.
    """
    try:
        df_dados = df_dados.copy()
        if chave_dados in df_dados.columns:
            df_dados[chave_dados] = df_dados[chave_dados].astype(str)
        if chave_geo in gdf_geo.columns:
            gdf_geo[chave_geo] = gdf_geo[chave_geo].astype(str)

        gdf_merged = gdf_geo.merge(df_dados, how='left', left_on=chave_geo, right_on=chave_dados)
        logger.info("Merge dos dados realizado com sucesso.")
        return gdf_merged
    except Exception as e:
        logger.error(f"Erro ao realizar o merge dos dados: {e}")
        return None

def calcular_metricas(gdf):
    """
    Calcula as métricas necessárias e adiciona ao GeoDataFrame.
    """
    try:
        colunas_numericas = ['trabalhados', 'nao_trabalhados', 'im_aegypti']
        for coluna in colunas_numericas:
            if coluna in gdf.columns:
                gdf[coluna] = pd.to_numeric(gdf[coluna], errors='coerce').fillna(0)

        gdf['tratamento_imoveis'] = gdf.apply(
            lambda row: row['trabalhados'] / (row['trabalhados'] + row['nao_trabalhados'])
            if (row['trabalhados'] + row['nao_trabalhados']) > 0 else 0,
            axis=1
        )

        gdf['nao_trabalhados_ratio'] = gdf.apply(
            lambda row: row['nao_trabalhados'] / (row['trabalhados'] + row['nao_trabalhados'])
            if (row['trabalhados'] + row['nao_trabalhados']) > 0 else 0,
            axis=1
        )

        gdf['incidencia_aedes'] = gdf.apply(
            lambda row: (row['im_aegypti'] / row['trabalhados']) * 1000
            if row['trabalhados'] > 0 else 0,
            axis=1
        )

        logger.info("Métricas calculadas com sucesso.")
        return gdf
    except Exception as e:
        logger.error(f"Erro ao calcular métricas: {e}")
        return None
