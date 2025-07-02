import requests
import pandas as pd
from io import StringIO
from urllib.parse import quote

# URL do endpoint
url = "http://compras.dados.gov.br/licitacoes/v1/orgaos.CSV?nome=turismo"

# Requisição HTTP
response = requests.get(url)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    # Converte o conteúdo em texto e lê como CSV
    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data, sep=';')  # ou sep=',' se o separador for vírgula

    # Exibe as primeiras linhas do DataFrame
    print(df.head())
else:
    print(f"Erro ao acessar o endpoint: {response.status_code}")
