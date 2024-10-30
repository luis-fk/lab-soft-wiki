import pandas as pd
import plotly.express as px
import plotly.io as pio

# Configurar o renderer padrão (opcional, dependendo do ambiente)
# Você pode definir o renderer para 'browser', 'notebook', etc.
# pio.renderers.default = 'browser'

# Carregar os dados dos arquivos CSV
tipo5_df = pd.read_csv('SAO_JOSE_DO_RIO_PRETO_tipo_5_dados.csv')
tipo6_df = pd.read_csv('SAO_JOSE_DO_RIO_PRETO_tipo_6_dados.csv')
tipo7_df = pd.read_csv('SAO_JOSE_DO_RIO_PRETO_tipo_7_dados.csv')

# Análise 1: Imóveis trabalhados vs não trabalhados por área
def analise_imoveis_trabalhados(tipo5_df):
    # Transformar o DataFrame para formato longo
    trabalhados_df_melted = tipo5_df.melt(id_vars='area', value_vars=['trabalhados', 'nao_trabalhados'],
                                          var_name='Status', value_name='Quantidade')
    # Renomear os valores de 'Status' para melhor legibilidade
    trabalhados_df_melted['Status'] = trabalhados_df_melted['Status'].replace({
        'trabalhados': 'Trabalhados',
        'nao_trabalhados': 'Não Trabalhados'
    })
    # Criar o gráfico de barras
    fig = px.bar(trabalhados_df_melted, x='area', y='Quantidade', color='Status',
                 barmode='group', title='Imóveis Trabalhados vs Não Trabalhados por Área')
    fig.update_layout(xaxis_title='Área', yaxis_title='Número de Imóveis')
    fig.show()

# Análise 2: im_larva por área
def analise_im_larva_por_area(tipo7_df):
    # Agrupar por 'area' e somar 'im_larva'
    larva_df = tipo7_df.groupby('area', as_index=False)['im_larva'].sum()
    # Criar o gráfico de barras
    fig = px.bar(larva_df, x='area', y='im_larva',
                 title='Número de Imóveis com Larvas Encontradas por Área')
    fig.update_layout(xaxis_title='Área', yaxis_title='Número de Imóveis com Larvas')
    fig.show()

# Análise 3: Visão somada - Imóveis trabalhados vs não trabalhados no município
def analise_imoveis_totais(tipo5_df):
    # Somar os totais de 'trabalhados' e 'nao_trabalhados'
    total_trabalhados = tipo5_df['trabalhados'].sum()
    total_nao_trabalhados = tipo5_df['nao_trabalhados'].sum()
    # Criar o DataFrame para o gráfico
    total_df = pd.DataFrame({
        'Status': ['Trabalhados', 'Não Trabalhados'],
        'Quantidade': [total_trabalhados, total_nao_trabalhados]
    })
    # Criar o gráfico de pizza
    fig = px.pie(total_df, names='Status', values='Quantidade',
                 title='Proporção de Imóveis Trabalhados vs Não Trabalhados no Município')
    fig.show()

# Análise 3 (continuação): Visão somada - Relação de larvas encontradas
def analise_larvas_totais(tipo7_df):
    # Somar o total de imóveis trabalhados e imóveis com larvas
    total_imoveis = tipo7_df['trabalhados'].sum()
    total_im_larva = tipo7_df['im_larva'].sum()
    # Calcular o número de imóveis sem larvas
    total_sem_larva = total_imoveis - total_im_larva
    # Criar o DataFrame para o gráfico
    larvas_df = pd.DataFrame({
        'Status': ['Imóveis com Larvas', 'Imóveis sem Larvas'],
        'Quantidade': [total_im_larva, total_sem_larva]
    })
    # Criar o gráfico de pizza
    fig = px.pie(larvas_df, names='Status', values='Quantidade',
                 title='Proporção de Imóveis com Larvas Encontradas no Município')
    fig.show()

# Chamar as funções de análise
analise_imoveis_trabalhados(tipo5_df)
analise_im_larva_por_area(tipo7_df)
analise_imoveis_totais(tipo5_df)
analise_larvas_totais(tipo7_df)
