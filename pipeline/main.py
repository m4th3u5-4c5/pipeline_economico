from datetime import date, datetime, timedelta

from coleta import buscar_serie
from carga import salvar, ultima_data

SERIES = {"dolar": 1}

def rodar():
    hoje = date.today() - timedelta(days=1)  # a API rejeita a data de hoje como data final
    for nome, codigo in SERIES.items():
        ultima = ultima_data(nome)
        if ultima:
            # incremental: começa no dia seguinte ao último guardado
            inicio = datetime.strptime(ultima, "%Y-%m-%d").date() + timedelta(days=1)
        else:
            inicio = date(2026, 1, 1)

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

if __name__ == "__main__":
    rodar()
    