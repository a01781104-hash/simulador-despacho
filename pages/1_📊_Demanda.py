import streamlit as st

st.set_page_config(page_title="Demanda CENACE", page_icon="📊", layout="wide")

st.title("📊 Demanda Horaria — CENACE")

st.markdown("""
Esta sección permite visualizar la **demanda eléctrica horaria real** descargada 
del sistema de CENACE para los tres sistemas eléctricos de México.
""")

st.markdown("---")

# --- Controles placeholder ---
col1, col2 = st.columns(2)

with col1:
    sistema = st.selectbox(
        "Sistema eléctrico",
        ["SIN", "BCA", "BCS"],
        help="SIN = Sistema Interconectado Nacional, BCA = Baja California, BCS = Baja California Sur"
    )

with col2:
    rango = st.date_input(
        "Rango de fechas",
        value=None,
        help="Selecciona el periodo de consulta"
    )

st.markdown("---")

# --- Placeholder para gráfica ---
st.subheader(f"Demanda horaria — {sistema}")
st.info("🚧 **Pendiente**: Integración con datos reales de CENACE (Semana 2).")
st.caption("Aquí se mostrará la gráfica de demanda horaria con datos descargados vía batching + caché.")

st.markdown("---")

# --- Placeholder para reporte de calidad ---
st.subheader("Reporte de calidad de datos")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("NaNs", "—")
with col2:
    st.metric("Negativos", "—")
with col3:
    st.metric("Huecos", "—")
with col4:
    st.metric("Cobertura", "—")

st.caption("Métricas de calidad se poblarán cuando el pipeline de datos esté activo.")
