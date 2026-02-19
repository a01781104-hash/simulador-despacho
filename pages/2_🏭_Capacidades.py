"""
Página 2: Capacidades Instaladas por Sistema
Tabla detallada con datos oficiales (PRODESEN/SENER) + caso 2026.
"""
import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Importar estilos compartidos
sys.path.insert(0, str(Path(__file__).parent.parent))
from styles import apply_styles, page_header, section, card, footer

st.set_page_config(page_title="Capacidades", page_icon="🏭", layout="wide")
apply_styles()

# ─── Header ───
page_header("🏭", "Capacidades Instaladas",
            "Capacidad por tecnología y sistema eléctrico — fuentes oficiales PRODESEN / SENER")

# ─── Cargar datos ───
DATA_DIR = Path(__file__).parent.parent / "data"

@st.cache_data
def load_capacity(filename):
    path = DATA_DIR / filename
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)

df_2024 = load_capacity("capacity_2024_by_system.csv")
df_2026 = load_capacity("capacity_2026_case.csv")

if df_2024.empty:
    st.error("⚠️ No se encontró `data/capacity_2024_by_system.csv`. "
             "Asegúrate de que el archivo existe en la carpeta `data/`.")
    st.stop()

# ─── Tabs: 2024 vs 2026 ───
tab1, tab2, tab3 = st.tabs(["📋 Caso Base 2024", "🔮 Proyección 2026", "📊 Comparativa"])

# ═══════════════════════════════════════════════
# TAB 1 — CASO BASE 2024
# ═══════════════════════════════════════════════
with tab1:
    section("Capacidad instalada — Caso Base 2024")

    # Selector de sistema
    sistemas = df_2024["sistema"].unique().tolist()
    sistema_sel = st.selectbox("Sistema eléctrico", sistemas, key="cap_2024_sys")

    df_sys = df_2024[df_2024["sistema"] == sistema_sel].copy()
    total_mw = df_sys["capacidad_mw"].sum()

    # KPI cards
    st.markdown("")
    kpi_cols = st.columns(3)
    with kpi_cols[0]:
        st.markdown(f"""
        <div class="card" style="text-align:center; padding:1rem;">
            <p style="font-size:1.5rem; font-weight:700; color:#00997A; margin:0;">
                {total_mw:,.0f} MW
            </p>
            <p style="font-size:0.75rem; color:#667788; margin:0.3rem 0 0; text-transform:uppercase; letter-spacing:0.05em;">
                Capacidad Total
            </p>
        </div>""", unsafe_allow_html=True)
    with kpi_cols[1]:
        renov = df_sys[df_sys["tecnologia"].isin(["Solar", "Eólica", "Hidro", "Geotérmica"])]["capacidad_mw"].sum()
        pct_renov = (renov / total_mw * 100) if total_mw > 0 else 0
        st.markdown(f"""
        <div class="card" style="text-align:center; padding:1rem;">
            <p style="font-size:1.5rem; font-weight:700; color:#00997A; margin:0;">
                {pct_renov:.1f}%
            </p>
            <p style="font-size:0.75rem; color:#667788; margin:0.3rem 0 0; text-transform:uppercase; letter-spacing:0.05em;">
                Renovable + Limpia
            </p>
        </div>""", unsafe_allow_html=True)
    with kpi_cols[2]:
        n_tech = len(df_sys)
        st.markdown(f"""
        <div class="card" style="text-align:center; padding:1rem;">
            <p style="font-size:1.5rem; font-weight:700; color:#00997A; margin:0;">
                {n_tech}
            </p>
            <p style="font-size:0.75rem; color:#667788; margin:0.3rem 0 0; text-transform:uppercase; letter-spacing:0.05em;">
                Tecnologías
            </p>
        </div>""", unsafe_allow_html=True)

    st.markdown("")

    # Dos columnas: tabla + gráfica
    col_table, col_chart = st.columns([1.1, 1])

    with col_table:
        st.markdown("**Detalle por tecnología**")
        df_display = df_sys[["tecnologia", "capacidad_mw", "costo_variable_usd_mwh", "fuente"]].copy()
        df_display.columns = ["Tecnología", "Capacidad (MW)", "Costo Variable (USD/MWh)", "Fuente"]
        df_display = df_display.sort_values("Capacidad (MW)", ascending=False).reset_index(drop=True)
        st.dataframe(df_display, use_container_width=True, hide_index=True, height=400)

    with col_chart:
        color_map = {
            "CCGT/Gas": "#2E86C1",
            "Carbón": "#5D6D7E",
            "Fuel Oil": "#E74C3C",
            "Diésel/Peaker": "#E67E22",
            "Hidro": "#00997A",
            "Solar": "#F4D03F",
            "Eólica": "#85C1E9",
            "Nuclear": "#8E44AD",
            "Geotérmica": "#D35400",
            "Batería": "#1ABC9C",
        }
        fig = px.pie(
            df_sys,
            values="capacidad_mw",
            names="tecnologia",
            color="tecnologia",
            color_discrete_map=color_map,
            hole=0.45,
        )
        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            font=dict(family="DM Sans, sans-serif"),
            legend=dict(orientation="v", yanchor="middle", y=0.5),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            textfont_size=11,
        )
        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════
# TAB 2 — PROYECCIÓN 2026
# ═══════════════════════════════════════════════
with tab2:
    section("Proyección 2026 — Crecimiento esperado")

    if df_2026.empty:
        st.warning("No se encontró `data/capacity_2026_case.csv`.")
    else:
        sistema_sel_26 = st.selectbox("Sistema eléctrico", df_2026["sistema"].unique().tolist(), key="cap_2026_sys")
        df_sys_26 = df_2026[df_2026["sistema"] == sistema_sel_26].copy()
        total_26 = df_sys_26["capacidad_mw"].sum()

        # KPIs
        df_sys_24_compare = df_2024[df_2024["sistema"] == sistema_sel_26]
        total_24 = df_sys_24_compare["capacidad_mw"].sum() if not df_sys_24_compare.empty else 0
        delta = total_26 - total_24
        delta_pct = (delta / total_24 * 100) if total_24 > 0 else 0

        kpi26 = st.columns(3)
        with kpi26[0]:
            st.metric("Capacidad 2026", f"{total_26:,.0f} MW", delta=f"+{delta:,.0f} MW")
        with kpi26[1]:
            st.metric("Crecimiento vs 2024", f"+{delta_pct:.1f}%")
        with kpi26[2]:
            renov_26 = df_sys_26[df_sys_26["tecnologia"].isin(
                ["Solar", "Eólica", "Hidro", "Geotérmica", "Batería"]
            )]["capacidad_mw"].sum()
            pct_renov_26 = (renov_26 / total_26 * 100) if total_26 > 0 else 0
            st.metric("% Renovable + Limpia", f"{pct_renov_26:.1f}%")

        st.markdown("")

        # Tabla con supuestos
        st.markdown("**Detalle con supuestos de cambio**")
        df_26_display = df_sys_26[["tecnologia", "capacidad_mw", "costo_variable_usd_mwh", "supuesto_cambio"]].copy()
        df_26_display.columns = ["Tecnología", "Capacidad (MW)", "Costo (USD/MWh)", "Supuesto de cambio"]
        df_26_display = df_26_display.sort_values("Capacidad (MW)", ascending=False).reset_index(drop=True)
        st.dataframe(df_26_display, use_container_width=True, hide_index=True)

        # Supuestos documentados
        with st.expander("📖 Ver supuestos completos (growth_assumptions.md)"):
            assumptions_path = DATA_DIR / "growth_assumptions.md"
            if assumptions_path.exists():
                st.markdown(assumptions_path.read_text(encoding="utf-8"))
            else:
                st.info("Archivo `growth_assumptions.md` no encontrado en `data/`.")

# ═══════════════════════════════════════════════
# TAB 3 — COMPARATIVA 2024 vs 2026
# ═══════════════════════════════════════════════
with tab3:
    section("Comparativa 2024 vs 2026")

    if df_2026.empty:
        st.warning("Se requiere el caso 2026 para la comparativa.")
    else:
        sistema_comp = st.selectbox("Sistema eléctrico", sistemas, key="cap_comp_sys")

        df_24_c = df_2024[df_2024["sistema"] == sistema_comp][["tecnologia", "capacidad_mw"]].copy()
        df_24_c = df_24_c.rename(columns={"capacidad_mw": "2024"})

        df_26_c = df_2026[df_2026["sistema"] == sistema_comp][["tecnologia", "capacidad_mw"]].copy()
        df_26_c = df_26_c.rename(columns={"capacidad_mw": "2026"})

        df_comp = pd.merge(df_24_c, df_26_c, on="tecnologia", how="outer").fillna(0)
        df_comp["Δ MW"] = df_comp["2026"] - df_comp["2024"]
        df_comp["Δ %"] = ((df_comp["2026"] - df_comp["2024"]) / df_comp["2024"].replace(0, 1) * 100).round(1)

        # Grouped bar chart
        df_melt = df_comp.melt(
            id_vars=["tecnologia"],
            value_vars=["2024", "2026"],
            var_name="Año",
            value_name="Capacidad (MW)",
        )

        color_year = {"2024": "#B0BEC5", "2026": "#00997A"}

        fig_comp = px.bar(
            df_melt,
            x="tecnologia",
            y="Capacidad (MW)",
            color="Año",
            barmode="group",
            color_discrete_map=color_year,
        )
        fig_comp.update_layout(
            xaxis_title="",
            yaxis_title="Capacidad Instalada (MW)",
            height=420,
            margin=dict(l=60, r=20, t=20, b=60),
            font=dict(family="DM Sans, sans-serif"),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="#e8ecf0"),
            yaxis=dict(gridcolor="#e8ecf0"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig_comp, use_container_width=True)

        # Delta table
        st.markdown("**Cambios por tecnología**")
        df_comp_display = df_comp.rename(columns={"tecnologia": "Tecnología"})
        st.dataframe(
            df_comp_display.sort_values("Δ MW", ascending=False).reset_index(drop=True),
            use_container_width=True,
            hide_index=True,
        )

# ─── Explicación ───
st.markdown("---")
section("¿Qué hace esta página?")

st.markdown("""
Esta página define **cuánta capacidad tiene cada sistema** por tipo de tecnología. Es clave porque:

1. **Caso 2024**: Establece el punto de partida con datos oficiales reales (PRODESEN/SENER).
2. **Caso 2026**: Permite simular el impacto del crecimiento de renovables y cambios en la matriz.
3. Los datos de aquí se usan directamente en el modelo PyPSA como `p_nom` (potencia nominal) de cada generador.
4. La trazabilidad es obligatoria — cada número tiene fuente documentada.

**Fuentes:** PRODESEN 2024-2038, PLADESE 2025-2039, SENER, CRE, CENACE Informe Pormenorizado 2023.
""")

footer()
