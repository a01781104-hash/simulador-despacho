"""
Página 1: Demanda CENACE
Descarga y visualización de demanda horaria real por sistema eléctrico.
Integra cenace_client (Musi) con diseño UX del equipo (Marifer & María).
"""
import sys
from pathlib import Path
from datetime import date, timedelta

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ─── Setup ───
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from cenace_client import get_demanda_total_sistema, validate_demand_data

# Importar estilos compartidos
sys.path.insert(0, str(Path(__file__).parent.parent))
from styles import apply_styles, page_header, section, card, footer

st.set_page_config(page_title="Demanda CENACE", page_icon="📊", layout="wide")
apply_styles()

# ─── Header ───
page_header("📊", "Demanda CENACE",
            "Descarga y visualización de demanda horaria real por sistema eléctrico")

# ─── Parámetros de consulta (en body, no sidebar) ───
section("Parámetros de consulta")

col_sys, col_ini, col_fin = st.columns([1.2, 1, 1])

sistemas_opciones = {
    "SIN": "SIN — Sistema Interconectado Nacional",
    "BCA": "BCA — Baja California",
    "BCS": "BCS — Baja California Sur",
}

with col_sys:
    sistema_sel = st.selectbox(
        "Sistema eléctrico",
        options=list(sistemas_opciones.keys()),
        format_func=lambda x: sistemas_opciones[x],
        index=0,
    )

hoy = date.today()
default_fin = hoy - timedelta(days=1)
default_ini = default_fin - timedelta(days=6)

with col_ini:
    fecha_ini = st.date_input("Fecha inicio", value=default_ini)
with col_fin:
    fecha_fin = st.date_input("Fecha fin", value=default_fin)

# Validaciones
if fecha_ini > fecha_fin:
    st.error("⚠️ La fecha de inicio debe ser anterior a la fecha fin.")
    st.stop()

if (fecha_fin - fecha_ini).days > 31:
    st.warning("⚠️ Rango mayor a 31 días — la descarga puede tomar varios minutos.")

# Opciones avanzadas
with st.expander("⚙️ Opciones avanzadas", expanded=False):
    col_cache, col_proceso = st.columns(2)
    with col_cache:
        use_cache = st.checkbox("Usar caché", value=True,
                                help="No repite llamadas a CENACE para datos ya descargados.")
    with col_proceso:
        proceso = st.selectbox("Tipo de proceso", ["MDA", "MTR"],
                               help="MDA = Mercado del Día en Adelanto, MTR = Mercado de Tiempo Real")

# Botón de descarga
st.markdown("")  # spacer
btn_descargar = st.button("🔄  Descargar datos de CENACE", type="primary", use_container_width=True)

st.markdown("---")

# ─── KPI Cards (siempre visibles) ───
kpi_cols = st.columns(4)
kpi_labels = ["HORAS DESCARGADAS", "DEMANDA MÁX (MW)", "DEMANDA MÍN (MW)", "COBERTURA"]

# Inicializar valores
kpi_values = ["—", "—", "—", "—"]

if "demand_data" in st.session_state and sistema_sel in st.session_state["demand_data"]:
    df = st.session_state["demand_data"][sistema_sel]
    report = validate_demand_data(df)
    kpi_values = [
        str(len(df)),
        f"{df['total_cargas_mw'].max():,.0f}",
        f"{df['total_cargas_mw'].min():,.0f}",
        f"{report['coverage_pct']}%",
    ]

for i, col in enumerate(kpi_cols):
    with col:
        st.markdown(f"""
        <div class="card" style="text-align:center; padding: 1.2rem 1rem;">
            <p style="font-size: 1.5rem; font-weight: 700; color: #00997A; margin: 0;">
                {kpi_values[i]}
            </p>
            <p style="font-size: 0.75rem; color: #667788; margin: 0.3rem 0 0 0;
                       letter-spacing: 0.05em; text-transform: uppercase;">
                {kpi_labels[i]}
            </p>
        </div>
        """, unsafe_allow_html=True)

# ─── Descarga ───
if btn_descargar:
    st.markdown("")
    progress_bar = st.progress(0, text=f"Conectando con CENACE ({sistema_sel})...")

    def update_progress(current, total):
        pct = current / total
        progress_bar.progress(pct, text=f"{sistema_sel}: batch {current}/{total}")

    try:
        df = get_demanda_total_sistema(
            sistema=sistema_sel,
            fecha_ini=fecha_ini.strftime("%Y-%m-%d"),
            fecha_fin=fecha_fin.strftime("%Y-%m-%d"),
            proceso=proceso,
            use_cache=use_cache,
            progress_callback=update_progress,
        )

        if df.empty:
            st.warning(f"No se obtuvieron datos para {sistema_sel}.")
            progress_bar.empty()
            st.stop()

        # Guardar en session_state
        if "demand_data" not in st.session_state:
            st.session_state["demand_data"] = {}
        st.session_state["demand_data"][sistema_sel] = df

        progress_bar.progress(1.0, text=f"{sistema_sel}: ✅ Descarga completa")
        st.rerun()

    except Exception as e:
        st.error(f"Error descargando {sistema_sel}: {e}")
        progress_bar.empty()

# ─── Gráfica y resultados ───
if "demand_data" in st.session_state and sistema_sel in st.session_state["demand_data"]:
    df = st.session_state["demand_data"][sistema_sel]

    section("Demanda horaria por sistema")

    colors = {"SIN": "#00997A", "BCA": "#E67E22", "BCS": "#2E86C1"}

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df["total_cargas_mw"],
        name=sistema_sel,
        mode="lines",
        line=dict(color=colors.get(sistema_sel, "#00997A"), width=2),
        fill="tozeroy",
        fillcolor=f"rgba({','.join(str(int(colors.get(sistema_sel, '#00997A').lstrip('#')[i:i+2], 16)) for i in (0, 2, 4))}, 0.08)",
        hovertemplate=(
            f"<b>{sistema_sel}</b><br>"
            "Fecha: %{x|%Y-%m-%d %H:%M}<br>"
            "Demanda: %{y:,.1f} MW<extra></extra>"
        ),
    ))

    fig.update_layout(
        xaxis_title="Fecha / Hora",
        yaxis_title="Demanda Total (MW)",
        hovermode="x unified",
        height=450,
        margin=dict(l=60, r=20, t=20, b=60),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#e8ecf0", showgrid=True),
        yaxis=dict(gridcolor="#e8ecf0", showgrid=True),
        font=dict(family="DM Sans, sans-serif"),
    )

    st.plotly_chart(fig, use_container_width=True)

    # ─── Reporte de calidad ───
    section("Reporte de calidad de datos")

    report = validate_demand_data(df)

    qual_cols = st.columns(4)
    with qual_cols[0]:
        st.metric("Cobertura", f"{report['coverage_pct']}%")
    with qual_cols[1]:
        st.metric("Huecos", report["missing_hours"])
    with qual_cols[2]:
        st.metric("Duplicados", report["duplicate_hours"])
    with qual_cols[3]:
        st.metric("Negativos", report["negative_values"])

    if report["date_range"]:
        st.caption(f"Rango: {report['date_range'][0]} → {report['date_range'][1]}")

    # Alertas de calidad
    if report["missing_hours"] > 0:
        st.warning(f"⚠️ Se detectaron {report['missing_hours']} horas faltantes.")
    if report["negative_values"] > 0:
        st.warning(f"⚠️ Se detectaron {report['negative_values']} valores negativos.")
    if report["nan_values"] > 0:
        st.warning(f"⚠️ Se detectaron {report['nan_values']} valores NaN.")
    if (report["missing_hours"] == 0 and report["negative_values"] == 0
            and report["nan_values"] == 0):
        st.success("✅ Datos sin problemas detectados.")

    # ─── Datos crudos + Export ───
    st.markdown("---")
    with st.expander("🔍 Ver datos crudos"):
        df_display = df[["timestamp", "total_cargas_mw"]].rename(
            columns={"timestamp": "Fecha/Hora", "total_cargas_mw": "Demanda (MW)"}
        )
        st.dataframe(df_display, use_container_width=True, height=300)

        # Botón de descarga CSV
        csv = df_display.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Descargar CSV",
            data=csv,
            file_name=f"demanda_{sistema_sel}_{fecha_ini}_{fecha_fin}.csv",
            mime="text/csv",
        )

else:
    st.markdown("""
    <div style="background: #f0faf6; border: 1px dashed #00997A; border-radius: 12px;
                padding: 2rem; text-align: center; color: #667788; margin-top: 1rem;">
        <p style="font-size: 1.1rem; margin: 0;">
            Selecciona los parámetros arriba y haz clic en
            <strong style="color: #00997A;">Descargar datos de CENACE</strong> para comenzar.
        </p>
    </div>
    """, unsafe_allow_html=True)

footer()
