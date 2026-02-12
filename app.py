import streamlit as st

st.set_page_config(
    page_title="Simulador de Despacho Económico — México",
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ Simulador de Despacho Económico para México")
st.subheader("CENACE · PyPSA · Streamlit")

st.markdown("---")

st.markdown("""
### ¿Qué es este simulador?

Esta aplicación permite simular el **despacho económico horario** de los tres sistemas 
eléctricos aislados de México:

- **SIN** — Sistema Interconectado Nacional  
- **BCA** — Baja California  
- **BCS** — Baja California Sur  

El simulador utiliza **datos reales de demanda de CENACE** y resuelve un problema de 
optimización de despacho económico usando **PyPSA**.
""")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Sistemas modelados", value="3")
    st.caption("SIN · BCA · BCS")

with col2:
    st.metric(label="Tecnologías", value="7+")
    st.caption("Solar, Eólica, Gas, Carbón, Diésel, Hidro, Batería")

with col3:
    st.metric(label="Escenarios predefinidos", value="5")
    st.caption("Fuel shock, VRE boom, Outage, Storage, Scarcity")

st.markdown("---")

st.markdown("""
### Navegación

Usa el **menú lateral izquierdo** (←) para navegar entre las secciones:

| Sección | Descripción |
|---|---|
| 📊 Demanda | Visualiza la demanda horaria real de CENACE |
| ⚡ Capacidades | Capacidad instalada por tecnología y sistema |
| 🔧 Despacho | Resultados de la optimización del despacho |
| 💰 Sensibilidad | Varía costos marginales y observa el impacto |
| 🎯 Escenarios | 5 escenarios predefinidos con lecciones |
| 📖 Metodología | Supuestos, limitaciones y fuentes |
""")

st.markdown("---")

st.info("🚧 **Proyecto en desarrollo** — Semana 1: Skeleton y estructura base.")

st.markdown("""
### Equipo
- *[Nombre 1]* — Project Leader  
- *[Nombre 2]* — Data Pipeline  
- *[Nombre 3]* — Modelo PyPSA  
- *[Nombre 4]* — Frontend/UX  
- *[Nombre 5]* — [Rol]  
- *[Nombre 6]* — [Rol]  
""")
