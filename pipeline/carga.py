import sqlite3
import pandas as pd

DB = "indicadores.db"

def salvar(df, nome_serie):
    conn = sqlite3.connect(DB)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS indicadores (
            serie TEXT NOT NULL,
            data TEXT NOT NULL,
            valor REAL NOT NULL,
            PRIMARY KEY (serie, data)
        )"""
    )
    df = df.assign(serie=nome_serie, data=df["data"].dt.strftime("%Y-%m-%d"))
    for linha in df[["serie", "data", "valor"]].itertuples(index=False):
        conn.execute(
            "INSERT OR REPLACE INTO indicadores VALUES (?, ?, ?)", tuple(linha)
        )
    conn.commit()
    conn.close()

def ultima_data(nome_serie):
    conn = sqlite3.connect(DB)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS indicadores (
            serie TEXT NOT NULL, data TEXT NOT NULL, valor REAL NOT NULL,
            PRIMARY KEY (serie, data))"""
    )
    r = conn.execute(
        "SELECT MAX(data) FROM indicadores WHERE serie = ?", (nome_serie,)
    ).fetchone()[0]
    conn.close()
    return r