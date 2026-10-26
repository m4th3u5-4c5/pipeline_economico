from fastapi.testclient import TestClient
import pandas as pd
import api.main as api_main
import carga

def test_api_serie(tmp_path, monkeypatch):
    db = str(tmp_path / "teste.db")
    monkeypatch.setattr(carga, "DB", db)
    monkeypatch.setattr(api_main, "DB", db)
    carga.salvar(pd.DataFrame({
        "data": pd.to_datetime(["2026-10-01", "2026-10-02"]),
        "valor": [5.0, 5.1],
    }), "dolar")

    client = TestClient(api_main.app)
    r = client.get("/indicadores/dolar")
    assert r.status_code == 200
    assert len(r.json()) == 2
    assert client.get("/indicadores/inexistente").status_code == 404