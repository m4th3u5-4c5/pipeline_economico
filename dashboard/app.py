import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st

DB = "indicadores.db"

st.set_page_config(page_title="Indicadores do Brasil", page_icon="📈", layout="wide")
st.title("📈 Indicadores Econômicos do Brasil")
st.caption("Fonte: Banco Central do Brasil (SGS)")

@st.cache_data(ttl=300)
def carregar():
    conn = sqlite3.connect(DB)
    df = pd.read_sql("SELECT serie, data, valor FROM indicadores ORDER BY data", conn)
    conn.close()
    df["data"] = pd.to_datetime(df["data"])
    return df

df = carregar()

if df.empty:
    st.warning("Banco vazio. Rode `python pipeline/main.py` primeiro.")
    st.stop()

ROTULOS = {"dolar": "Dólar (R$)", "selic": "Selic (% a.a.)", "ipca": "IPCA (% mensal)"}

# cartões com o último valor e a variação em relação ao registro anterior
colunas = st.columns(len(ROTULOS))
for col, (serie, rotulo) in zip(colunas, ROTULOS.items()):
    d = df[df["serie"] == serie]
    if len(d) >= 2:
        ultimo, anterior = d["valor"].iloc[-1], d["valor"].iloc[-2]
        col.metric(rotulo, f"{ultimo:.2f}", f"{ultimo - anterior:+.2f}")
    elif len(d) == 1:
        col.metric(rotulo, f"{d['valor'].iloc[-1]:.2f}")

st.divider()

escolhida = st.selectbox("Série", list(ROTULOS), format_func=lambda s: ROTULOS[s])
d = df[df["serie"] == escolhida]

inicio, fim = st.slider(
    "Período",
    min_value=d["data"].min().date(),
    max_value=d["data"].max().date(),
    value=(d["data"].min().date(), d["data"].max().date()),
)
d = d[(d["data"].dt.date >= inicio) & (d["data"].dt.date <= fim)]

fig = px.line(d, x="data", y="valor", title=ROTULOS[escolhida])
fig.update_layout(xaxis_title="", yaxis_title="")
st.plotly_chart(fig, use_container_width=True)

with st.expander("Ver dados"):
    st.dataframe(d.sort_values("data", ascending=False), use_container_width=True)