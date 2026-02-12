import streamlit as st

st.set_page_config(page_title="Escenarios", page_icon="🎯", layout="wide")

st.title("🎯 Escenarios Predefinidos")

st.markdown("""
Selecciona uno de los **5 escenarios predefinidos** para explorar distintas condiciones 
del sistema eléctrico. Cada escenario cambia un conjunto de parámetros y produce 
una lección interpretable.
""")

st.markdown("---")

# --- Selector de escenario ---
escenario = st.selectbox(
    "Selecciona un escenario",
    [
        "1. Fuel Price Shock — Gas/Diésel ↑",
        "2. Renewables Boom 2026 — Solar/Eólica ↑ capacidad",
        "3. Forced Outage — Térmica clave ↓",
        "4. Add Storage — Batería activa",
        "5. Scarcity Knob — VOLL ↑/↓",
    ]
)

st.markdown("---")

# --- Info por escenario ---
escenarios_info = {
    "1. Fuel Price Shock — Gas/Diésel ↑": {
        "cambio": "Costos marginales térmicos aumentan significativamente.",
        "leccion": "Sensibilidad de precios y despacho a combustibles; quién marca precio.",
        "parametros": "Gas: 45→80, Diésel: 150→250 USD/MWh",
    },
    "2. Renewables Boom 2026 — Solar/Eólica ↑ capacidad": {
        "cambio": "Capacidades VRE aumentan al caso 2026.",
        "leccion": "Curtailment y necesidad de flexibilidad; no todo MW VRE reduce costos.",
        "parametros": "Solar y Eólica → capacidades caso 2026",
    },
    "3. Forced Outage — Térmica clave ↓": {
        "cambio": "Reducción de capacidad de una térmica clave (ej. 30% de CCGT offline).",
        "leccion": "Confiabilidad y riesgo; cuándo aparece shedding y cuánto cuesta evitarlo.",
        "parametros": "CCGT p_nom → 70% del base",
    },
    "4. Add Storage — Batería activa": {
        "cambio": "Se activa batería con tamaño configurable por sistema.",
        "leccion": "Arbitraje, reducción de picos, valor depende de spreads y VRE.",
        "parametros": "Batería: 500 MW / 2000 MWh (configurable)",
    },
    "5. Scarcity Knob — VOLL ↑/↓": {
        "cambio": "Penalización de load shedding varía.",
        "leccion": "Tradeoff costo vs confiabilidad; política implícita cambia decisiones.",
        "parametros": "VOLL: 2,000 → 10,000 USD/MWh",
    },
}

info = escenarios_info[escenario]

st.subheader(escenario)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**Qué cambia:** {info['cambio']}")
    st.markdown(f"**Parámetros:** `{info['parametros']}`")
with col2:
    st.markdown(f"**Lección esperada:** {info['leccion']}")

st.markdown("---")

if st.button("▶️ Ejecutar escenario", type="primary"):
    st.info("🚧 **Pendiente**: Ejecución de escenarios con PyPSA (Semana 9).")

st.markdown("---")

# --- Placeholder resultados ---
st.subheader("Resultados del escenario")
st.caption("1 gráfico + 3 bullets por escenario: cambio, resultado, implicación")
st.info("🚧 Pendiente.")
