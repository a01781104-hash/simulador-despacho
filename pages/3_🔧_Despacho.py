import streamlit as st

st.set_page_config(page_title="Despacho Económico", page_icon="🔧", layout="wide")

st.title("🔧 Resultados del Despacho Económico")

st.markdown("""
Esta sección muestra los **resultados de la optimización** del despacho económico 
resuelto con PyPSA (solver HiGHS). Se presenta el despacho por tecnología, 
curtailment, load shedding y precio marginal.
""")

st.markdown("---")

# --- Controles ---
col1, col2 = st.columns(2)

with col1:
    sistema = st.selectbox("Sistema", ["SIN", "BCA", "BCS"])
with col2:
    fecha = st.date_input("Fecha de despacho", value=None)

if st.button("▶️ Ejecutar despacho", type="primary"):
    st.info("🚧 **Pendiente**: Integración con modelo PyPSA (Semana 4).")

st.markdown("---")

# --- Placeholder resultados ---
st.subheader("Despacho por tecnología (MW)")
st.caption("Gráfica de área apilada — generación por tecnología por hora")
st.info("🚧 Gráfica pendiente.")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Curtailment (MW)")
    st.caption("VRE disponible vs. utilizada")
    st.info("🚧 Pendiente (Semana 7).")

with col2:
    st.subheader("Load Shedding (MW)")
    st.caption("Demanda no atendida, si ocurre")
    st.info("🚧 Pendiente (Semana 4).")

st.markdown("---")

st.subheader("KPIs del despacho")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Costo total", "— USD")
with col2:
    st.metric("Precio marginal promedio", "— USD/MWh")
with col3:
    st.metric("Curtailment total", "— MWh")
with col4:
    st.metric("Load shedding total", "— MWh")

st.markdown("---")

st.subheader("Precio marginal (Shadow Price)")
st.caption("Precio marginal por hora y sistema")
st.info("🚧 **Pendiente**: Extracción de shadow prices (Semana 5).")
