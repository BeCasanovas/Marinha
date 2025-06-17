import requests
import pandas as pd
from time import sleep

UASG = 771300
BASE_URL = "https://compras.dados.gov.br"
LIMIT = 50
MAX_PAGES = 5  # você pode aumentar depois

resultados = []

for page in range(1, MAX_PAGES + 1):
    url = f"{BASE_URL}/licitacoes/v1/licitacoes.json?uasg={UASG}&offset={(page - 1) * LIMIT}&limit={LIMIT}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erro ao acessar página {page}: {response.status_code}")
        break

    data = response.json()
    licitacoes = data.get("licitacoes", [])

    print(f"Página {page} retornou {len(licitacoes)} pregões")

    for lic in licitacoes:
        id_pregao = lic.get("id_licitacao")
        numero_pregao = lic.get("numero_aviso")

        if not id_pregao:
            continue

        pregao_url = f"{BASE_URL}/pregoes/id/pregao/{id_pregao}.json"
        pregao_resp = requests.get(pregao_url)
        if pregao_resp.status_code != 200:
            print(f"Erro ao acessar pregão {id_pregao}")
            continue

        pregao_data = pregao_resp.json()
        data_homologacao = pregao_data.get("dataHomologacao")
        valor_total = pregao_data.get("valorHomologadoTotal")

        itens_url = f"{BASE_URL}/pregoes/id/pregao/{id_pregao}/itens.json"
        itens_resp = requests.get(itens_url)
        if itens_resp.status_code != 200:
            print(f"Erro ao acessar itens do pregão {id_pregao}")
            continue

        itens_data = itens_resp.json()
        print(f"Pregão {numero_pregao}: {len(itens_data)} itens")

        for item in itens_data:
            resultados.append({
                "numero_pregao": numero_pregao,
                "numero_item": item.get("numero_item"),
                "valor_homologado": item.get("valor_homologado_item"),
                "marca_modelo": item.get("descricao_material_servico", "N/A"),
                "data_homologacao": data_homologacao,
                "empresa_vencedora": item.get("nome_fornecedor", "N/A"),
                "cnpj": item.get("cnpj_fornecedor", "N/A"),
            })

        sleep(0.5)  # evita sobrecarregar a API

# Após coleta, verificar se houve resultados
if not resultados:
    print("Nenhum resultado encontrado.")
else:
    df = pd.DataFrame(resultados)
    df.to_excel("pregoes_COMRJ.xlsx", index=False)
    print(f"{len(df)} registros salvos em pregoes_COMRJ.xlsx")
