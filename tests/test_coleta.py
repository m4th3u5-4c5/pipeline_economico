import pytest
import requests
import coleta

class FakeResp:
    def __init__(self, status=200, payload=None):
        self.status_code = status
        self._payload = payload

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(response=self)

def test_parse_dados(monkeypatch):
    payload = [{"data": "02/01/2026", "valor": "5.4372"}]
    monkeypatch.setattr(coleta.requests, "get", lambda *a, **k: FakeResp(200, payload))
    df = coleta.buscar_serie(1, "01/01/2026", "02/01/2026")
    assert len(df) == 1
    assert df["valor"].iloc[0] == 5.4372

def test_404_vira_dataframe_vazio(monkeypatch):
    monkeypatch.setattr(coleta.requests, "get", lambda *a, **k: FakeResp(404))
    df = coleta.buscar_serie(1, "24/10/2026", "25/10/2026")
    assert df.empty

def test_resposta_de_erro_esgota_tentativas(monkeypatch):
    monkeypatch.setattr(coleta.requests, "get", lambda *a, **k: FakeResp(200, {"erro": {}}))
    monkeypatch.setattr(coleta.time, "sleep", lambda s: None)
    with pytest.raises(RuntimeError):
        coleta.buscar_serie(1, "01/01/2026", "26/10/2026")