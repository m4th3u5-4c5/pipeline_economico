import requests
import pandas as pd

URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"

def buscar_serie(codigo, data_inicial, data_final):
    """Busca uma série do SGS do Banco Central.
    Datas no formato dd/mm/aaaa."""
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
    df = pd.DataFrame(resp.json())
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
    df["valor"] = pd.to_numeric(df["valor"])
    return df

if __name__ == "__main__":
    # série 1 = dólar (venda). Confere o código no site do BCB se quiser garantir.
    df = buscar_serie(1, "01/01/2026", "31/10/2026")
    print(df.tail(10))
    print(f"\n{len(df)} registros")