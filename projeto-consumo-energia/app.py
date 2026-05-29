import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ─── Configuração da página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Consumo de Energia Elétrica no Brasil",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS customizado ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    .kpi-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-left: 4px solid #f39c12;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        color: white;
    }
    .kpi-value { font-size: 1.8rem; font-weight: 700; color: #f39c12; }
    .kpi-label { font-size: 0.85rem; color: #adb5bd; margin-bottom: 0.2rem; }
    .section-title {
        font-size: 1.2rem; font-weight: 600;
        border-bottom: 2px solid #f39c12;
        padding-bottom: 0.4rem; margin-bottom: 1rem;
    }
    .insight-box {
        background-color: #f8f9fa;
        border-left: 4px solid #3498db;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ─── Carregamento dos dados ───────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("dados/simulacao_consumo_energia_brasil.csv", parse_dates=["data"])
    return df

df_raw = load_data()

# ─── Sidebar — Filtros ────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/lightning-bolt.png", width=60)
    st.title("⚡ Filtros")
    st.markdown("---")

    anos = sorted(df_raw["ano"].unique())
    ano_sel = st.multiselect("📅 Ano", anos, default=anos)

    meses = sorted(df_raw["mes"].unique())
    mes_sel = st.multiselect("🗓️ Mês", meses, default=meses,
                              format_func=lambda m: ["Jan","Fev","Mar","Abr","Mai","Jun",
                                                      "Jul","Ago","Set","Out","Nov","Dez"][m-1])

    regioes = sorted(df_raw["regiao"].unique())
    regiao_sel = st.multiselect("🗺️ Região", regioes, default=regioes)

    ufs = sorted(df_raw["uf"].unique())
    uf_sel = st.multiselect("📍 Estado (UF)", ufs, default=ufs)

    setores = sorted(df_raw["setor_consumo"].unique())
    setor_sel = st.multiselect("🏭 Setor de Consumo", setores, default=setores)

    niveis = sorted(df_raw["nivel_demanda"].unique())
    nivel_sel = st.multiselect("📊 Nível de Demanda", niveis, default=niveis)

    st.markdown("---")
    st.caption("Projeto G2 — Tema 14 | Análise de Energia Elétrica no Brasil (2015–2024)")

# ─── Aplicar filtros ──────────────────────────────────────────────────────────
df = df_raw[
    df_raw["ano"].isin(ano_sel) &
    df_raw["mes"].isin(mes_sel) &
    df_raw["regiao"].isin(regiao_sel) &
    df_raw["uf"].isin(uf_sel) &
    df_raw["setor_consumo"].isin(setor_sel) &
    df_raw["nivel_demanda"].isin(nivel_sel)
].copy()

# ─── Cabeçalho ────────────────────────────────────────────────────────────────
st.title("⚡ Consumo de Energia Elétrica no Brasil")
st.markdown("**Análise exploratória de dados — 2015 a 2024** | Projeto G2 — Tema 14")
st.markdown(
    "Este dashboard analisa padrões de consumo de energia elétrica no Brasil, "
    "permitindo identificar regiões com maior demanda, sazonalidade, evolução temporal "
    "e relação entre temperatura e consumo."
)

if df.empty:
    st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados. Ajuste os filtros na barra lateral.")
    st.stop()

# ─── KPIs ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📌 Indicadores-Chave (KPIs)</div>', unsafe_allow_html=True)

consumo_total = df["consumo_mwh"].sum()
estado_top = df.groupby("uf")["consumo_mwh"].sum().idxmax()
setor_top = df.groupby("setor_consumo")["consumo_mwh"].sum().idxmax()
demanda_media = df["demanda_pico"].mean()
tarifa_media = df["tarifa_media"].mean()
co2_total = df["emissao_co2"].sum()

col1, col2, col3, col4, col5, col6 = st.columns(6)
kpis = [
    (col1, "Consumo Total", f"{consumo_total/1e6:.2f} TWh"),
    (col2, "Estado Top Consumo", estado_top),
    (col3, "Setor Líder", setor_top),
    (col4, "Demanda Média", f"{demanda_media:,.0f} MW"),
    (col5, "Tarifa Média", f"R$ {tarifa_media:.2f}/kWh"),
    (col6, "Emissão CO₂ Total", f"{co2_total/1e6:.2f} Mt"),
]
for col, label, value in kpis:
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Gráfico 1: Linha temporal ────────────────────────────────────────────────
st.markdown('<div class="section-title">📈 Evolução Temporal do Consumo</div>', unsafe_allow_html=True)
df_temporal = df.groupby(["ano", "mes"])["consumo_mwh"].sum().reset_index()
df_temporal["periodo"] = pd.to_datetime(df_temporal["ano"].astype(str) + "-" + df_temporal["mes"].astype(str) + "-01")
df_temporal = df_temporal.sort_values("periodo")

fig_linha = px.line(
    df_temporal, x="periodo", y="consumo_mwh",
    labels={"periodo": "Período", "consumo_mwh": "Consumo (MWh)"},
    title="Consumo Mensal de Energia Elétrica",
    color_discrete_sequence=["#f39c12"],
    markers=True,
)
fig_linha.update_layout(hovermode="x unified", plot_bgcolor="#f9f9f9")
st.plotly_chart(fig_linha, use_container_width=True)
st.markdown('<div class="insight-box">💡 <b>Interpretação:</b> A série temporal revela a tendência de crescimento do consumo ao longo dos anos, bem como variações sazonais (picos no verão e quedas no outono/inverno), típicas do comportamento energético brasileiro.</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Gráfico 2 & 3: Ranking estados + Setores ────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.markdown('<div class="section-title">🏆 Ranking de Consumo por Estado</div>', unsafe_allow_html=True)
    df_uf = df.groupby("uf")["consumo_mwh"].sum().sort_values(ascending=True).reset_index()
    fig_uf = px.bar(
        df_uf, x="consumo_mwh", y="uf", orientation="h",
        labels={"consumo_mwh": "Consumo (MWh)", "uf": "Estado"},
        color="consumo_mwh", color_continuous_scale="YlOrRd",
        title="Consumo Total por Estado"
    )
    fig_uf.update_layout(showlegend=False, coloraxis_showscale=False, plot_bgcolor="#f9f9f9")
    st.plotly_chart(fig_uf, use_container_width=True)
    st.markdown('<div class="insight-box">💡 Estados do Sudeste (SP, RJ, MG) concentram a maior fatia do consumo nacional, refletindo densidade industrial e populacional.</div>', unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="section-title">🏭 Consumo por Setor Econômico</div>', unsafe_allow_html=True)
    df_setor = df.groupby("setor_consumo")["consumo_mwh"].sum().reset_index()
    fig_setor = px.bar(
        df_setor.sort_values("consumo_mwh", ascending=True),
        x="consumo_mwh", y="setor_consumo", orientation="h",
        labels={"consumo_mwh": "Consumo (MWh)", "setor_consumo": "Setor"},
        color="setor_consumo",
        color_discrete_sequence=px.colors.qualitative.Bold,
        title="Consumo Total por Setor"
    )
    fig_setor.update_layout(showlegend=False, plot_bgcolor="#f9f9f9")
    st.plotly_chart(fig_setor, use_container_width=True)
    st.markdown('<div class="insight-box">💡 O setor Industrial tende a liderar o consumo, seguido do Residencial e Comercial, padrão consistente com economias em desenvolvimento.</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Gráfico 4: Dispersão temperatura x consumo ───────────────────────────────
st.markdown('<div class="section-title">🌡️ Relação entre Temperatura e Consumo</div>', unsafe_allow_html=True)
fig_disp = px.scatter(
    df, x="temperatura_media", y="consumo_mwh",
    color="regiao", size="demanda_pico",
    hover_data=["uf", "setor_consumo", "ano"],
    labels={"temperatura_media": "Temperatura Média (°C)", "consumo_mwh": "Consumo (MWh)", "regiao": "Região"},
    title="Temperatura Média vs. Consumo de Energia",
    opacity=0.65,
    color_discrete_sequence=px.colors.qualitative.Set2,
)
fig_disp.update_layout(plot_bgcolor="#f9f9f9")
st.plotly_chart(fig_disp, use_container_width=True)
st.markdown('<div class="insight-box">💡 Regiões com temperaturas mais altas (Norte e Nordeste) apresentam maior consumo per capita de energia, influenciado pelo uso intensivo de ar-condicionado e refrigeração.</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Gráfico 5: Heatmap mensal ────────────────────────────────────────────────
st.markdown('<div class="section-title">🗓️ Sazonalidade — Heatmap Mensal por Ano</div>', unsafe_allow_html=True)
df_heat = df.groupby(["ano", "mes"])["consumo_mwh"].sum().reset_index()
df_pivot = df_heat.pivot(index="ano", columns="mes", values="consumo_mwh")
df_pivot.columns = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

fig_heat = px.imshow(
    df_pivot,
    color_continuous_scale="YlOrRd",
    labels=dict(x="Mês", y="Ano", color="Consumo (MWh)"),
    title="Heatmap de Consumo Mensal por Ano",
    aspect="auto",
    text_auto=".2s",
)
fig_heat.update_layout(xaxis_side="top")
st.plotly_chart(fig_heat, use_container_width=True)
st.markdown('<div class="insight-box">💡 O heatmap evidencia a sazonalidade: meses de verão (Jan, Fev, Dez) e a tendência crescente de consumo ao longo dos anos.</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Gráfico 6: Comparação regional ──────────────────────────────────────────
st.markdown('<div class="section-title">🗺️ Comparação Regional ao Longo do Tempo</div>', unsafe_allow_html=True)
df_reg = df.groupby(["ano", "regiao"])["consumo_mwh"].sum().reset_index()
fig_reg = px.line(
    df_reg, x="ano", y="consumo_mwh", color="regiao",
    markers=True,
    labels={"ano": "Ano", "consumo_mwh": "Consumo (MWh)", "regiao": "Região"},
    title="Evolução do Consumo por Região",
    color_discrete_sequence=px.colors.qualitative.Set1,
)
fig_reg.update_layout(plot_bgcolor="#f9f9f9")
st.plotly_chart(fig_reg, use_container_width=True)
st.markdown('<div class="insight-box">💡 O Sudeste mantém o maior volume de consumo, mas o Centro-Oeste e Norte apresentam crescimento relativo acelerado, sinalizando expansão econômica nessas regiões.</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Gráfico 7: Eficiência energética ────────────────────────────────────────
st.markdown('<div class="section-title">♻️ Eficiência Energética por Região e Setor</div>', unsafe_allow_html=True)
df_efic = df.groupby(["regiao", "setor_consumo"])["eficiencia_energetica"].mean().reset_index()
fig_efic = px.bar(
    df_efic, x="regiao", y="eficiencia_energetica", color="setor_consumo",
    barmode="group",
    labels={"regiao": "Região", "eficiencia_energetica": "Eficiência Média (%)", "setor_consumo": "Setor"},
    title="Índice Médio de Eficiência Energética",
    color_discrete_sequence=px.colors.qualitative.Pastel,
)
fig_efic.update_layout(plot_bgcolor="#f9f9f9")
st.plotly_chart(fig_efic, use_container_width=True)
st.markdown('<div class="insight-box">💡 A eficiência energética varia significativamente entre regiões e setores. O setor Rural tende a apresentar menor eficiência, enquanto o Comercial e Industrial lideram nas métricas de aproveitamento.</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Tabela dinâmica ──────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📋 Tabela de Exploração Detalhada</div>', unsafe_allow_html=True)
cols_show = ["ano", "mes", "regiao", "uf", "setor_consumo", "consumo_mwh",
             "demanda_pico", "temperatura_media", "tarifa_media", "nivel_demanda", "emissao_co2"]
st.dataframe(
    df[cols_show].sort_values(["ano","mes"]).reset_index(drop=True),
    use_container_width=True,
    height=350,
)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Conclusão executiva ──────────────────────────────────────────────────────
st.markdown('<div class="section-title">📝 Conclusão Executiva</div>', unsafe_allow_html=True)
st.markdown(f"""
O Brasil apresentou crescimento consistente no consumo de energia elétrica entre 2015 e 2024,
com picos sazonais nos meses de verão e desaceleração pontual associada a eventos econômicos (ex.: pandemia em 2020).

- **Região Sudeste** concentra a maior demanda energética do país, liderada pelo estado de **SP**.
- O setor **Industrial** é o maior consumidor, seguido de Residencial e Comercial.
- **Temperatura e consumo** apresentam correlação positiva nas regiões Norte e Nordeste.
- O índice de **eficiência energética** cresceu ao longo do período, indicando melhora na gestão do consumo.
- As **emissões de CO₂** totalizaram **{co2_total/1e6:.2f} Mt** no período analisado, reforçando a necessidade de diversificação da matriz energética.

Ações recomendadas: investimento em energias renováveis nas regiões de maior crescimento (Norte e Centro-Oeste),
programas de eficiência energética no setor rural e residencial, e monitoramento de picos de demanda crítica.
""")

# ─── Rodapé ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("⚡ Projeto G2 — Tema 14 | Consumo de Energia Elétrica no Brasil | Desenvolvido com Python + Streamlit + Plotly")
