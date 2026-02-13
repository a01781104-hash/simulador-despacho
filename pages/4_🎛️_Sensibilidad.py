"""
🎛️ Sensibilidad de Costos
Sliders para ajustar costos marginales y observar impacto.
"""

import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import apply_styles, page_header, section, card, footer

st.set_page_config(page_title="Sensibilidad", page_icon="🎛️", layout="wide")
apply_styles()

page_header("🎛️", "Sensibilidad de Costos",
            "Ajusta costos marginales por tecnología y observa el impacto en el despacho")

# ── Sliders ───────────────────────────────────────────────────────
section("Costos marginales (USD/MWh)")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Térmicas**")
    gas = st.slider("🔥 CCGT / Gas", 30, 60, 45, help="Rango: 30–60 USD/MWh")
    carbon = st.slider("⬛ Carbón", 50, 70, 60, help="Rango: 50–70 USD/MWh")
    fuel_oil = st.slider("🛢️ Fuel oil / Pesada", 80, 120, 100, help="Rango: 80–120 USD/MWh")
    diesel = st.slider("⛽ Diésel / Peaker", 120, 180, 150, help="Rango: 120–180 USD/MWh")

with col2:
    st.markdown("**Otras**")
    hidro = st.slider("💧 Hidro", 0, 10, 5, help="Rango: 0–10 USD/MWh")
    solar = st.slider("☀️ Solar", 0, 5, 0, help="Costo marginal, no LCOE")
    eolica = st.slider("💨 Eólica", 0, 5, 0, help="Costo marginal, no LCOE")
    voll = st.slider("🚨 VOLL (shedding)", 2000, 10000, 5000, step=500,
                     help="Value of Lost Load: penalización por no servir demanda")

st.markdown("---")

# ── Resumen de configuración ──────────────────────────────────────
section("Configuración actual")

st.markdown(f"""
<div class="metric-row">
    <div class="metric-card">
        <p class="metric-value">${gas}</p>
        <p class="metric-label">Gas</p>
    </div>
    <div class="metric-card">
        <p class="metric-value">${carbon}</p>
        <p class="metric-label">Carbón</p>
    </div>
    <div class="metric-card">
        <p class="metric-value">${fuel_oil}</p>
        <p class="metric-label">Fuel oil</p>
    </div>
    <div class="metric-card">
        <p class="metric-value">${diesel}</p>
        <p class="metric-label">Diésel</p>
    </div>
    <div class="metric-card">
        <p class="metric-value">${voll:,}</p>
        <p class="metric-label">VOLL</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.info("🔜 **Semana 6** — Comparación antes/después al mover sliders: impacto en despacho, costo total y precio marginal.")

# ── Explicación ───────────────────────────────────────────────────
section("¿Qué hace esta página?")

st.markdown("""
Esta página permite hacer **análisis de sensibilidad**:

1. Mueves un slider (por ejemplo, subes el costo del gas).
2. El modelo re-optimiza el despacho con el nuevo costo.
3. Ves cómo cambia: qué tecnología genera más/menos, cómo sube o baja el costo total, y quién marca el precio marginal.

**Ejemplo**: Si subes el gas de $45 a $60, el modelo podría despachar más carbón (si es más barato) o más renovables. 
Esto demuestra la **sensibilidad** del sistema a los precios de combustibles.

Los rangos de los sliders vienen de la tabla de referencia del curso (orden de magnitud educativo, no costos reales por planta).
""")

footer()
