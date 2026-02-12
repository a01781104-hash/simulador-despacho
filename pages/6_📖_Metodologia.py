import streamlit as st

st.set_page_config(page_title="Metodología y Limitaciones", page_icon="📖", layout="wide")

st.title("📖 Metodología, Supuestos y Limitaciones")

st.markdown("---")

# --- Qué hace ---
st.subheader("¿Qué hace este simulador?")
st.markdown("""
Simula el **despacho económico horario** (merit order optimization) para los tres sistemas 
eléctricos aislados de México (SIN, BCA, BCS) usando datos reales de demanda de CENACE 
y el framework de optimización PyPSA con solver HiGHS.

El objetivo es **educativo**: entender cómo funciona el despacho económico, la sensibilidad 
a costos de combustibles, y el impacto de renovables y almacenamiento.
""")

st.markdown("---")

# --- Qué NO hace ---
st.subheader("⚠️ Qué NO modela (Limitaciones)")
st.markdown("""
Este simulador **no pretende replicar** el despacho real de CENACE. Las principales 
simplificaciones son:

- **Sin red de transmisión** — cada sistema es un bus único, sin restricciones de red ni flujos internos.
- **Sin unit commitment** — no modela arranques/paradas, rampas, mínimos técnicos por planta.
- **Sin reservas operativas** — no incluye reservas de frecuencia, spinning, ni regulación.
- **Sin restricciones N-1** — no modela contingencias ni seguridad de red.
- **Térmicas agregadas** — se agrupan plantas por tipo de combustible, no se modelan plantas individuales.
- **Hidro simplificada** — potencia fija + presupuesto energético diario, sin modelar embalse ni hidrología.
- **Perfiles VRE aproximados** — basados en coordenadas representativas (Renewables.ninja), no en plantas reales.
- **Sin costos de arranque/parada** — solo costos marginales variables.
- **Sin degradación de batería** — modelo simplificado de almacenamiento.
""")

st.markdown("---")

# --- Metodología ---
st.subheader("Metodología de despacho")
st.markdown("""
**Formulación:** Minimización del costo total de generación sujeto a:
- Balance de energía por hora y sistema (generación = demanda)
- Límites de capacidad por generador
- Disponibilidad horaria de VRE
- Presupuesto energético diario para hidro
- Restricciones SOC de batería

**Solver:** PyPSA ≥ 0.26 con `network.optimize()` (Linopy) + HiGHS

**Precio marginal:** Shadow price de la restricción de balance de energía por hora.
""")

st.markdown("---")

# --- Stack ---
st.subheader("Stack tecnológico")
st.markdown("""
| Componente | Tecnología |
|---|---|
| Lenguaje | Python |
| UI | Streamlit |
| Optimización | PyPSA + Linopy + HiGHS |
| Datos de demanda | API CENACE (batch + caché) |
| Perfiles VRE | Renewables.ninja |
| Visualización | Plotly |
| Datos | pandas, numpy |
""")

st.markdown("---")

# --- Fuentes ---
st.subheader("Fuentes de datos")
st.markdown("""
- **Demanda horaria:** CENACE — Sistema de Información del Mercado Eléctrico
- **Capacidades instaladas:** PRODESEN, SENER, CRE (por documentar en Semana 3)
- **Perfiles VRE:** Renewables.ninja (coordenadas en Sección 9 de la actividad)
- **Costos marginales:** Tabla de referencia del bloque (orden de magnitud educativo)
""")

st.markdown("---")

# --- Costos de referencia ---
st.subheader("Tabla de costos marginales de referencia (USD/MWh)")

import pandas as pd

costos = pd.DataFrame({
    "Tecnología": ["CCGT / Gas", "Carbón", "Fuel Oil", "Diésel / Peaker", "Hidro", 
                    "Solar / Eólica", "Batería", "VOLL (Shedding)"],
    "Rango (USD/MWh)": ["30–60", "50–70", "80–120", "120–180", "0–10", 
                          "0–5", "0–2", "2,000–10,000"],
    "Valor base usado": ["45", "60", "100", "150", "5", "0", "1", "5,000"],
})

st.dataframe(costos, use_container_width=True, hide_index=True)

st.caption("Estos rangos son orden de magnitud para simulación educativa, no representan costos por planta.")

st.markdown("---")

st.subheader("Unidades y convenciones")
st.markdown("""
- **Potencia:** MW  
- **Energía:** MWh  
- **Costos variables:** USD/MWh  
- **Moneda:** USD (cualquier conversión se documenta)  
- **Resolución temporal:** Horaria  
""")
