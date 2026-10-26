from datetime import date, datetime, timedelta

from coleta import buscar_serie
from carga import salvar, ultima_data

# Confere os códigos no site do BCB (SGS) antes de confiar neles
SERIES = {"dolar": 1, "selic": 432, "ipca": 433}

DATA_INICIAL = date(2026, 1, 1)

def rodar():
    # a API rejeita a data de hoje como data final, então usa ontem
    hoje = date.today() - timedelta(days=1)

    for nome, codigo in SERIES.items():
        try:
            ultima = ultima_data(nome)
            if ultima:
                # incremental: começa no dia seguinte ao último guardado
                inicio = datetime.strptime(ultima, "%Y-%m-%d").date() + timedelta(days=1)
            else:
                inicio = DATA_INICIAL

            if inicio > hoje:
                print(f"{nome}: já está atualizado")
                continue

            df = buscar_serie(
                codigo, inicio.strftime("%d/%m/%Y"), hoje.strftime("%d/%m/%Y")
            )
            if df.empty:
                print(f"{nome}: nenhum dado novo")
                continue

            salvar(df, nome)
            print(f"{nome}: {len(df)} registros novos salvos")
        except Exception as erro:
            # uma série com problema não derruba as outras
            print(f"{nome}: falhou ({erro})")

if __name__ == "__main__":
    rodar()