import streamlit as st

st.set_page_config(page_title="Capacidades Instaladas", page_icon="⚡", layout="wide")

st.title("⚡ Capacidad Instalada por Tecnología")

st.markdown("""
Aquí se muestra la **capacidad instalada (MW)** por tecnología y sistema eléctrico, 
basada en fuentes oficiales. Se incluye un caso base (2024) y un caso prospectivo (2026).
""")

st.markdown("---")

# --- Selector de escenario ---
caso = st.radio(
    "Caso de capacidad",
    ["Base 2024", "Crecimiento esperado 2026"],
    horizontal=True,
    help="El caso 2026 incluye supuestos documentados de crecimiento en growth_assumptions.md"
)

st.markdown("---")

# --- Placeholder tabla ---
st.subheader(f"Capacidades — {caso}")
st.info("🚧 **Pendiente**: Carga de datos desde `capacity_2024_by_system.csv` y `capacity_2026_case.csv` (Semana 3).")

# Tabla ejemplo de estructura esperada
import pandas as pd

ejemplo = pd.DataFrame({
    "Tecnología": ["CCGT/Gas", "Carbón", "Fuel Oil", "Diésel", "Hidro", "Solar", "Eólica", "Batería"],
    "SIN (MW)": ["—"] * 8,
    "BCA (MW)": ["—"] * 8,
    "BCS (MW)": ["—"] * 8,
})

st.dataframe(ejemplo, use_container_width=True, hide_index=True)

st.caption("Fuentes: PRODESEN, SENER, CRE — por documentar en Semana 3.")

st.markdown("---")

st.subheader("Supuestos de crecimiento (caso 2026)")
st.info("🚧 **Pendiente**: Documentación en `growth_assumptions.md` (Semana 3).")
