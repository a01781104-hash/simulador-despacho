import streamlit as st

st.set_page_config(page_title="Sensibilidad de Costos", page_icon="💰", layout="wide")

st.title("💰 Análisis de Sensibilidad — Costos Marginales")

st.markdown("""
Ajusta los **costos marginales por tecnología** usando los sliders y observa cómo 
cambia el despacho, el costo total y el precio marginal.
""")

st.markdown("---")

# --- Sliders de costos ---
st.subheader("Costos marginales (USD/MWh)")

col1, col2 = st.columns(2)

with col1:
    gas = st.slider("CCGT / Gas", min_value=20, max_value=100, value=45, step=5)
    carbon = st.slider("Carbón", min_value=30, max_value=100, value=60, step=5)
    fuel_oil = st.slider("Fuel Oil / Térmica pesada", min_value=50, max_value=150, value=100, step=5)

with col2:
    diesel = st.slider("Diésel / Peaker", min_value=80, max_value=250, value=150, step=10)
    hidro = st.slider("Hidro", min_value=0, max_value=20, value=5, step=1)
    voll = st.slider("VOLL (Load Shedding)", min_value=1000, max_value=15000, value=5000, step=500)

st.markdown("---")

st.caption(f"Gas: {gas} · Carbón: {carbon} · Fuel Oil: {fuel_oil} · Diésel: {diesel} · Hidro: {hidro} · VOLL: {voll}")

if st.button("▶️ Re-ejecutar despacho con nuevos costos", type="primary"):
    st.info("🚧 **Pendiente**: Conexión con modelo PyPSA para re-optimizar (Semana 6).")

st.markdown("---")

# --- Placeholder comparación ---
st.subheader("Comparación: Base vs. Ajustado")
st.info("🚧 Pendiente: gráficas comparativas antes/después (Semana 6).")
