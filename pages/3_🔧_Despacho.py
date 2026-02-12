"""
🔧 Despacho Económico
Modelo de optimización PyPSA y resultados.

PARA EL EQUIPO (Jime & Alexa):
- Esta página ejecuta y muestra los resultados del modelo PyPSA.
- La UI está lista; ustedes conectan el modelo.
"""

import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import apply_styles, page_header, section, card, footer

st.set_page_config(page_title="Despacho", page_icon="🔧", layout="wide")
apply_styles()

page_header("🔧", "Despacho Económico",
            "Optimización del despacho horario con PyPSA + HiGHS — mínimo costo")

# ── Controles ────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    st.selectbox("Sistema", ["SIN", "BCA", "BCS"])
with col2:
    st.selectbox("Período", ["1 día", "3 días", "1 semana"])
with col3:
    st.selectbox("Caso de capacidades", ["Base 2024", "Proyección 2026"])

run = st.button("▶️ Ejecutar despacho", type="primary", use_container_width=True)

st.markdown("---")

# ── Resultados ────────────────────────────────────────────────────
section("Resultados del despacho")

st.markdown("""
<div class="metric-row">
    <div class="metric-card">
        <p class="metric-value">—</p>
        <p class="metric-label">Costo Total (USD)</p>
    </div>
    <div class="metric-card">
        <p class="metric-value">—</p>
        <p class="metric-label">Curtailment (MWh)</p>
    </div>
    <div class="metric-card">
        <p class="metric-value">—</p>
        <p class="metric-label">Shedding (MWh)</p>
    </div>
    <div class="metric-card">
        <p class="metric-value">—</p>
        <p class="metric-label">Precio marginal prom.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.info("🔜 **Semana 4** — Gráfica de stacked area: generación por tecnología hora por hora.")

# ── Shadow price ──────────────────────────────────────────────────
section("Precio marginal (Shadow Price)")

st.info("🔜 **Semana 5** — Gráfica de precio marginal por hora e interpretación económica.")

card("¿Qué es el shadow price?",
     "Es el costo de producir un MWh adicional en cada hora. "
     "Refleja el costo marginal de la tecnología más cara que está generando. "
     "Si hay shedding, el precio sube al VOLL.")

# ── Explicación ───────────────────────────────────────────────────
section("¿Qué hace esta página?")

st.markdown("""
Esta es la **página central** del simulador. Aquí ocurre la optimización:

1. Toma la **demanda** (de la página CENACE) y las **capacidades** (de la página Capacidades).
2. Resuelve el **problema de despacho** con PyPSA: minimizar el costo total de generación respetando límites de cada tecnología.
3. Muestra los **resultados**: qué tecnología genera cuánto en cada hora, si hay curtailment de renovables o load shedding.
4. Calcula el **precio marginal** (shadow price) que indica el costo de satisfacer un MW adicional de demanda.

La fórmula básica: **min Σ (costo_marginal × generación)** sujeto a que generación = demanda en cada hora.
""")

footer()
