import sqlite3

import pandas as pd
import carga

def _df():
    return pd.DataFrame({
        "data": pd.to_datetime(["2026-10-01", "2026-10-02"]),
        "valor": [5.0, 5.1],
    })

def test_salvar_nao_duplica(tmp_path, monkeypatch):
    monkeypatch.setattr(carga, "DB", str(tmp_path / "teste.db"))
    carga.salvar(_df(), "dolar")
    carga.salvar(_df(), "dolar")  # salva de novo
    conn = sqlite3.connect(carga.DB)
    total = conn.execute("SELECT COUNT(*) FROM indicadores").fetchone()[0]
    conn.close()
    assert total == 2

def test_ultima_data(tmp_path, monkeypatch):
    monkeypatch.setattr(carga, "DB", str(tmp_path / "teste.db"))
    assert carga.ultima_data("dolar") is None
    carga.salvar(_df(), "dolar")
    assert carga.ultima_data("dolar") == "2026-10-02"