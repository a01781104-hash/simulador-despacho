"""
📊 Demanda CENACE
Descarga y visualización de demanda horaria real.

PARA EL EQUIPO (Alexa & Musi):
- Esta página muestra la demanda horaria descargada de CENACE.
- Ustedes conectan el pipeline de datos real (Semana 2).
- La UI ya tiene los controles y placeholders listos.
"""

import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import apply_styles, page_header, section, card, footer

st.set_page_config(page_title="Demanda CENACE", page_icon="📊", layout="wide")
apply_styles()

# ── Header ───────────────────────────────────────────────────────
page_header("📊", "Demanda CENACE", "Descarga y visualización de demanda horaria real por sistema eléctrico")

# ── Controles ────────────────────────────────────────────────────
section("Parámetros de consulta")

col1, col2, col3 = st.columns(3)
with col1:
    sistema = st.selectbox("Sistema eléctrico", ["SIN", "BCA", "BCS"])
with col2:
    fecha_inicio = st.date_input("Fecha inicio")
with col3:
    fecha_fin = st.date_input("Fecha fin")

st.markdown("---")

# ── Estado ────────────────────────────────────────────────────────
st.markdown("""
<div class="metric-row">
    <div class="metric-card">
        <p class="metric-value">—</p>
        <p class="metric-label">Horas descargadas</p>
    </div>
    <div class="metric-card">
        <p class="metric-value">—</p>
        <p class="metric-label">Demanda máx (MW)</p>
    </div>
    <div class="metric-card">
        <p class="metric-value">—</p>
        <p class="metric-label">Demanda mín (MW)</p>
    </div>
    <div class="metric-card">
        <p class="metric-value">—</p>
        <p class="metric-label">Cobertura</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Gráfica placeholder ──────────────────────────────────────────
section("Demanda horaria por sistema")

st.info("🔜 **Semana 2** — Aquí aparecerá la gráfica de demanda horaria real descargada de CENACE.")

# ── Reporte de calidad ────────────────────────────────────────────
section("Reporte de calidad de datos")

col1, col2 = st.columns(2)
with col1:
    card("Validaciones automáticas",
         "NaN detectados · Valores negativos · Huecos temporales · "
         "Duplicados por DST · Cobertura del período")
with col2:
    card("Pipeline de datos",
         "Batching en ventanas ≤ 7 días · Caché en disco · "
         "Reintentos ante fallos · Fallback a caché · Consistencia temporal")

# ── Explicación ───────────────────────────────────────────────────
section("¿Qué hace esta página?")

st.markdown("""
Esta página es la **entrada de datos** del simulador. Su función es:

1. **Descargar** demanda horaria real desde la API de CENACE para el sistema y fechas seleccionados.
2. **Validar** la calidad de los datos: detectar huecos, duplicados por cambio de horario (DST), valores negativos o NaN.
3. **Visualizar** la curva de demanda para verificar que los datos tienen sentido.
4. **Cachear** los datos en disco para no repetir descargas y hacer la app más rápida.

Los datos de esta página alimentan al modelo de despacho en la sección "Despacho".
""")

footer()
