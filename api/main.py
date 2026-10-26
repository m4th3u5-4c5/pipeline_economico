import sqlite3
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="Pipeline Econômico", description="Indicadores do Banco Central")
DB = "indicadores.db"

def consultar(sql, params=()):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    try:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]
    finally:
        conn.close()

@app.get("/")
def raiz():
    return {"status": "ok", "docs": "/docs"}

@app.get("/indicadores")
def listar_indicadores():
    return consultar(
        "SELECT serie, COUNT(*) AS registros, MIN(data) AS inicio, MAX(data) AS fim "
        "FROM indicadores GROUP BY serie"
    )

@app.get("/indicadores/{serie}")
def obter_serie(
    serie: str,
    inicio: str = Query(None, description="AAAA-MM-DD"),
    fim: str = Query(None, description="AAAA-MM-DD"),
):
    sql = "SELECT data, valor FROM indicadores WHERE serie = ?"
    params = [serie]
    if inicio:
        sql += " AND data >= ?"
        params.append(inicio)
    if fim:
        sql += " AND data <= ?"
        params.append(fim)
    sql += " ORDER BY data"
    dados = consultar(sql, params)
    if not dados:
        raise HTTPException(status_code=404, detail="Série não encontrada ou sem dados")
    return dados