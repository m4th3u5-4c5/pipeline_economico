import time
import requests
import pandas as pd

URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"

def buscar_serie(codigo, data_inicial, data_final, tentativas=4, espera=3):
    """Busca uma série do SGS do Banco Central, com retry.
    Datas no formato dd/mm/aaaa."""
    for n in range(1, tentativas + 1):
        try:
            resp = requests.get(
                URL.format(codigo=codigo),
                params={
                    "formato": "json",
                    "dataInicial": data_inicial,
                    "dataFinal": data_final,
                },
                timeout=30,
            )
            resp.raise_for_status()
            dados = resp.json()
            if isinstance(dados, list):
                if not dados:
                    return pd.DataFrame(columns=["data", "valor"])
                df = pd.DataFrame(dados)
                df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
                df["valor"] = pd.to_numeric(df["valor"])
                return df
            print(f"[tentativa {n}] resposta inesperada da API: {str(dados)[:100]}")
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                # BCB devolve 404 quando não há dados no período (ex.: fim de semana)
                return pd.DataFrame(columns=["data", "valor"])
            print(f"[tentativa {n}] erro HTTP: {e}")
        except requests.RequestException as e:
            print(f"[tentativa {n}] erro de rede: {e}")
        time.sleep(espera * n)  # espera cada vez mais
    raise RuntimeError("API do BCB não respondeu com dados válidos")

if __name__ == "__main__":
    df = buscar_serie(1, "01/01/2026", "25/10/2026")
    print(df.tail(10))
    print(f"\n{len(df)} registros")