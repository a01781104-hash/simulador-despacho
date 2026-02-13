"""
🏭 Capacidades Instaladas
Capacidad por tecnología y sistema (2024 y 2026).

PARA EL EQUIPO:
- Los datos vienen de fuentes oficiales (PRODESEN, SENER, CENACE).
- El caso 2026 requiere supuestos documentados en growth_assumptions.md.
"""

import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import apply_styles, page_header, section, card, footer

st.set_page_config(page_title="Capacidades", page_icon="🏭", layout="wide")
apply_styles()

page_header("🏭", "Capacidades Instaladas",
            "Capacidad instalada por tecnología y sistema eléctrico — caso 2024 y proyección 2026")

# ── Tabs ──────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📋 Caso Base 2024", "📈 Proyección 2026"])

with tab1:
    section("Capacidad instalada 2024 — Fuentes oficiales")
    
    st.markdown("""
    <div class="metric-row">
        <div class="metric-card">
            <p class="metric-value">~85 GW</p>
            <p class="metric-label">SIN Total</p>
        </div>
        <div class="metric-card">
            <p class="metric-value">~4 GW</p>
            <p class="metric-label">BCA Total</p>
        </div>
        <div class="metric-card">
            <p class="metric-value">~1 GW</p>
            <p class="metric-label">BCS Total</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🔜 **Semana 3** — Tabla detallada con capacidades por tecnología desde fuentes oficiales (PRODESEN, SENER).")
    
    card("Tecnologías modeladas",
         "CCGT/Gas · Carbón · Fuel oil · Diésel/Peaker · "
         "Solar · Eólica · Hidro · Batería · Load shedding (VOLL)")

with tab2:
    section("Proyección 2026 — Crecimiento esperado")
    
    st.info("🔜 **Semana 3** — Capacidades proyectadas a 2026 con supuestos documentados.")
    
    card("Supuestos requeridos",
         "Cada cambio respecto al caso 2024 debe estar justificado y documentado "
         "en growth_assumptions.md con fuente y razonamiento.")

# ── Explicación ───────────────────────────────────────────────────
section("¿Qué hace esta página?")

st.markdown("""
Esta página define **cuánta capacidad tiene cada sistema** por tipo de tecnología. Es clave porque:

1. **Caso 2024**: Establece el punto de partida con datos oficiales reales.
2. **Caso 2026**: Permite simular el impacto del crecimiento de renovables y cambios en la matriz.
3. Los datos de aquí se usan directamente en el modelo PyPSA como `p_nom` (potencia nominal) de cada generador.
4. La trazabilidad es obligatoria — cada número debe tener fuente.
""")

footer()
