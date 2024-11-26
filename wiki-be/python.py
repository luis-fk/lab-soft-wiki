import requests
import pandas as pd

# Função para extrair dados da API com o parâmetro censitário
def extrair_dados_api(tipo, municipio_id, data_inicio, data_fim, execucao, censitario, incluir_imoveis=False):
    # URL base da API
    base_url = "https://vigent.saude.sp.gov.br/sisaweb_api/dados.php"
    
    # Parâmetros da requisição
    params = {
        "tipo": tipo,
        "id": municipio_id,
        "inicio": data_inicio,
        "final": data_fim,
        "exec": execucao,
        "censitario": censitario
    }
    
    # Adiciona o parâmetro 'im' se incluir_imoveis for True
    if incluir_imoveis:
        params["im"] = 1
    
    # Faz a requisição para a API
    response = requests.get(base_url, params=params)
    
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        try:
            return response.json()  # Tenta retornar os dados como JSON
        except ValueError:
            print(f"Erro ao decodificar JSON para o tipo {tipo}.")
            return None
    else:
        print(f"Erro na requisição para o tipo {tipo}. Status code: {response.status_code}")
        return None

# Função para organizar os dados em um DataFrame
def organizar_dados_em_tabela(dados, tipo):
    if dados is None or len(dados) == 0:
        return pd.DataFrame()  # Retorna um DataFrame vazio se não houver dados
    
    # Converte o JSON em DataFrame (ajustar com base no formato dos dados recebidos)
    df = pd.DataFrame(dados)
    
    # Adiciona uma coluna para identificar o tipo de dado
    df['tipo'] = tipo
    
    return df

# Parâmetros iniciais
tipos_dados = [1, 2, 3, 4, 5,6,7,8,9,10,11,12,13,14,15,16]  # Exemplo de tipos de dados a serem coletados
municipio_id = 465  # ID do município de interesse
data_inicio = "2022-10-20"
data_fim = "2024-10-20"
execucao = 2  # Defina o valor de execução adequado
censitario = 1  # Valor do parâmetro censitário
incluir_imoveis = True  # Opcional: definir se quer incluir imóveis detalhados

# Lista para armazenar todos os DataFrames
tabelas = []

# Loop para coletar dados para cada tipo
for tipo in tipos_dados:
    print(f"Extraindo dados do tipo {tipo}...")
    dados = extrair_dados_api(tipo, municipio_id, data_inicio, data_fim, execucao, censitario, incluir_imoveis)
    if dados:
        df_tipo = organizar_dados_em_tabela(dados, tipo)
        if not df_tipo.empty:
            tabelas.append(df_tipo)
        else:
            print(f"Sem dados disponíveis para o tipo {tipo}.")
    else:
        print(f"Falha ao extrair dados para o tipo {tipo}.")

# Concatena todos os DataFrames em um único DataFrame, caso haja dados
if tabelas:
    df_final = pd.concat(tabelas, ignore_index=True)
    # Salva o DataFrame final em um arquivo CSV
    df_final.to_csv("dados_api_4.csv", index=False)
    print("Dados extraídos e salvos com sucesso!")
else:
    print("Nenhum dado foi extraído.")

