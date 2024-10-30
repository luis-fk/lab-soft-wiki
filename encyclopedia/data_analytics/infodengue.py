import requests
import pandas as pd

class InfoDengueAPI:
    BASE_URL = "https://info.dengue.mat.br/api/alertcity"

    def __init__(self):
        # Adiciona várias cidades do estado de São Paulo
        self.geocode_map = {
            "São Paulo": "3550308",
            "Campinas": "3509502",
            "Santos": "3548500",
            "Sorocaba": "3552206",
            "Ribeirão Preto": "3543402",
            "São José dos Campos": "3549904",
            "Guarulhos": "3518800",
            "Osasco": "3534401",
            "Jundiaí": "3525904",
            "Bauru": "3506003",
            "São Carlos": "3548906",
            "Franca": "3516200",
            "Piracicaba": "3538709",
            "Presidente Prudente": "3541406",
            "São Vicente": "3551000",
            "Mogi das Cruzes": "3543303",
            "Belo Horizonte": "3106200",
            "Rio de Janeiro": "3304557",
            "Salvador": "2927408",
            "Fortaleza": "2304400",
            "Recife": "2611606",
            "Porto Alegre": "4314902",
            "Curitiba": "4106902",
            "Manaus": "1302603",
            "Belém": "1501402",
            "Goiânia": "5208707",
            "Campo Grande": "5002704",
            "Natal": "2408102",
            "João Pessoa": "2507507",
            "Maceió": "2704302",
            "Aracaju": "2800308",
            "Cuiabá": "5103403",
            "Palmas": "1721000",
            "Macapá": "1600303",
            "Rio Branco": "1200401",
            "Boa Vista": "1400100",
            "Porto Velho": "1100205",
            "Teresina": "2211001",
            "São Luís": "2111300",
            "Caxias do Sul": "4204103",
            "Florianópolis": "4205407",
            "Joinville": "4209102",
            "Criciuma": "4204608",
            "Londrina": "4113700",
            "São José do Rio Preto": "3549805",
            "Araraquara": "3503208",
            "Marília": "3529005",
            "São Bernardo do Campo": "3548708",
            "Barretos": "3505500",
            "Araçatuba": "3502804"
        }
    def get_geocode(self, city_name):
        """Converte o nome da cidade para o geocode IBGE."""
        geocode = self.geocode_map.get(city_name)
        if not geocode:
            raise ValueError(f"Geocode não encontrado para a cidade '{city_name}'")
        return geocode

    def fetch_dengue_alerts(self, city_name, disease, ew_start, ew_end, ey_start, ey_end, format="json"):
        """Consulta a API InfoDengue para alertas com os parâmetros especificados."""
        geocode = self.get_geocode(city_name)
        params = {
            "geocode": geocode,
            "disease": disease,
            "format": format,
            "ew_start": ew_start,
            "ew_end": ew_end,
            "ey_start": ey_start,
            "ey_end": ey_end
        }
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json() if format == "json" else response.text
        return data

    def export_to_csv(self, data, filename="dengue_alerts.csv"):
        """Exporta os dados da API para um arquivo CSV."""
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Dados exportados para {filename}")

# Caso de teste aprimorado com exportação para CSV
def test_fetch_and_export_dengue_alerts():
    api = InfoDengueAPI()
    try:
        # Consulta para a cidade de São Paulo, com exportação de resultados para CSV
        data = api.fetch_dengue_alerts(
            city_name="São José do Rio Preto",
            disease="dengue",
            ew_start=1,
            ew_end=50,
            ey_start=2020,
            ey_end=2020,
            format="json"
        )
        # Exporta para CSV
        api.export_to_csv(data, "dengue_alerts_sao_jose_do_rio_preto.csv")
        print("Teste e exportação bem-sucedidos!")
    except Exception as e:
        print(f"Erro no teste: {e}")

# Executa o caso de teste
test_fetch_and_export_dengue_alerts()
