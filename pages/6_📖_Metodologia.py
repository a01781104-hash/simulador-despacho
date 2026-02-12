"""
📖 Metodología y Documentación
Qué hace el simulador, qué no hace, fuentes y supuestos.
"""

import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import apply_styles, page_header, section, card, footer

st.set_page_config(page_title="Metodología", page_icon="📖", layout="wide")
apply_styles()

page_header("📖", "Metodología y Documentación",
            "Supuestos, limitaciones, fuentes de datos y documentación técnica del simulador")

# ── Qué hace ──────────────────────────────────────────────────────
section("✅ Qué hace este simulador")

col1, col2 = st.columns(2)
with col1:
    card("Datos", "Descarga demanda horaria real de CENACE para SIN, BCA y BCS con batching y caché.")
    card("Modelo", "Resuelve un despacho económico de mínimo costo usando PyPSA + HiGHS.")
    card("Interactividad", "Permite variar costos marginales desde sliders y ver el impacto en tiempo real.")
with col2:
    card("Sistemas", "Modela cada sistema como un bus independiente sin interconexión entre ellos.")
    card("Escenarios", "Compara 5 escenarios predefinidos con lecciones claras sobre el sistema eléctrico.")
    card("Resultados", "Muestra generación por tecnología, curtailment, shedding, costos y precios marginales.")

# ── Limitaciones ──────────────────────────────────────────────────
section("❌ Limitaciones — Qué NO modela")

st.markdown("""
| Limitación | Detalle |
|:-----------|:--------|
| **Sin red interna** | No modela flujos de potencia entre nodos dentro de un sistema |
| **Sin interconexión** | SIN, BCA y BCS son completamente aislados |
| **Sin unit commitment** | No considera arranque/paro, rampas ni mínimos técnicos |
| **Sin reservas** | No modela regulación, spinning ni reservas operativas |
| **Sin contingencias** | No aplica criterio N-1 ni análisis de contingencias |
| **Hidro simplificado** | Potencia fija + energy budget diario, sin modelar embalse |
| **Batería simplificada** | SOC + eficiencia + límites, sin degradación ni cycling cost complejo |
| **Costos educativos** | Rangos de orden de magnitud, no costos reales por planta |
""")

# ── Stack ─────────────────────────────────────────────────────────
section("🛠️ Stack tecnológico")

st.markdown("""
| Componente | Herramienta | Versión |
|:-----------|:-----------|:--------|
| Lenguaje | Python | 3.10+ |
| Interfaz web | Streamlit | ≥ 1.30 |
| Optimización | PyPSA + Linopy | ≥ 0.26 |
| Solver | HiGHS | Incluido con Linopy |
| Datos demanda | API CENACE | — |
| Perfiles VRE | Renewables.ninja | — |
| Visualización | Plotly | — |
""")

# ── Fuentes ───────────────────────────────────────────────────────
section("📚 Fuentes de datos")

col1, col2 = st.columns(2)
with col1:
    card("Demanda", "CENACE — Sistema de Información del Mercado (API pública). Resolución horaria.")
    card("Capacidades", "PRODESEN, SENER, reportes de CENACE. Fuentes oficiales del gobierno de México.")
with col2:
    card("Perfiles VRE", "Renewables.ninja — perfiles solares y eólicos por coordenadas representativas de cada sistema.")
    card("Costos marginales", "Rangos de referencia del curso en USD/MWh. Orden de magnitud para simulación educativa.")

# ── Supuestos ─────────────────────────────────────────────────────
section("📌 Supuestos clave")

st.markdown("""
- **Sistemas aislados**: SIN, BCA y BCS son buses independientes sin interconexión.
- **Resolución temporal**: Horaria (1h), consistente con datos CENACE.
- **Costos marginales en USD/MWh** como unidad base (conversiones documentadas).
- **Generadores agregados**: Térmicas en 2–4 categorías (CCGT, carbón, fuel oil, diésel).
- **Hidro**: Límite de potencia fijo (`p_nom`) + energy budget diario (MWh/día).
- **Batería**: SOC + eficiencia + límites. Sin degradación.
- **VOLL**: 2,000–10,000 USD/MWh como penalización de load shedding.
- **Solver**: PyPSA ≥ 0.26 con `network.optimize(solver_name='highs')`.
""")

# ── Costos de referencia ──────────────────────────────────────────
section("💵 Tabla de costos de referencia")

st.markdown("""
| Tecnología | Rango (USD/MWh) | Nota |
|:-----------|:---------------|:-----|
| CCGT / Gas | 30–60 | — |
| Carbón | 50–70 | — |
| Fuel oil / Pesada | 80–120 | — |
| Diésel / Peaker | 120–180 | — |
| Hidro | 0–10 | — |
| Solar / Eólica | 0–5 | Costo marginal, no LCOE |
| Batería | 0–2 | Costo marginal de operación |
| VOLL (shedding) | 2,000–10,000 | Penalización por demanda no servida |
""")

st.caption("Estos rangos son de orden de magnitud para simulación educativa; no representan costos por planta.")

# ── Coordenadas VRE ───────────────────────────────────────────────
section("🌍 Coordenadas para perfiles VRE")

st.markdown("""
| Sistema | Recurso | Coordenadas | Referencia |
|:--------|:--------|:-----------|:-----------|
| SIN | Solar | 29.1°N, 110.9°W | Sonora (alta irradiación) |
| SIN | Eólica | 16.5°N, 95.0°W | Istmo de Tehuantepec |
| BCA | Solar | 32.5°N, 115.5°W | Mexicali / norte de BC |
| BCA | Eólica | 31.8°N, 116.6°W | La Rumorosa |
| BCS | Solar | 24.1°N, 110.3°W | La Paz |
| BCS | Eólica | 24.8°N, 111.9°W | Sur de BCS |
""")

footer()
