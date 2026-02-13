"""
📈 Escenarios Predefinidos
5 presets con lecciones claras del sistema eléctrico.
"""

import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import apply_styles, page_header, section, footer

st.set_page_config(page_title="Escenarios", page_icon="📈", layout="wide")
apply_styles()

page_header("📈", "Escenarios Predefinidos",
            "5 presets para explorar lecciones clave del despacho económico")

# ── Escenarios ────────────────────────────────────────────────────
escenarios = [
    {
        "icon": "🔥", "nombre": "Fuel Price Shock",
        "tag_color": "tag-red", "tag": "Precios",
        "desc": "Gas y diésel suben de precio drásticamente.",
        "cambia": "Costos marginales térmicos ↑",
        "leccion": "Sensibilidad de precios y despacho a combustibles. Muestra quién marca el precio marginal y cómo cascadea un shock de precios.",
    },
    {
        "icon": "☀️", "nombre": "Renewables Boom 2026",
        "tag_color": "tag-green", "tag": "Capacidad",
        "desc": "Capacidad solar y eólica aumentan al caso 2026.",
        "cambia": "Capacidades VRE ↑ (caso 2026)",
        "leccion": "Curtailment y necesidad de flexibilidad. No todo MW de renovables reduce costos — sin almacenamiento, se desperdicia energía.",
    },
    {
        "icon": "⚠️", "nombre": "Forced Outage",
        "tag_color": "tag-orange", "tag": "Confiabilidad",
        "desc": "Una térmica clave pierde capacidad (falla o mantenimiento).",
        "cambia": "Capacidad firme ↓",
        "leccion": "Confiabilidad y riesgo. Muestra cuándo aparece el shedding y cuánto cuesta evitarlo. Evidencia la importancia de la reserva.",
    },
    {
        "icon": "🔋", "nombre": "Add Storage",
        "tag_color": "tag-blue", "tag": "Flexibilidad",
        "desc": "Se activa batería con tamaño configurable.",
        "cambia": "Batería activa con parámetros ajustables",
        "leccion": "Arbitraje temporal: la batería carga cuando hay exceso renovable (bajo costo) y descarga en picos. Su valor depende de los spreads de precio.",
    },
    {
        "icon": "💰", "nombre": "Scarcity Knob (VOLL)",
        "tag_color": "tag-gray", "tag": "Política",
        "desc": "Se modifica la penalización de load shedding.",
        "cambia": "VOLL ↑ o ↓",
        "leccion": "Tradeoff costo vs confiabilidad. Un VOLL alto dice 'nunca cortes' — un VOLL bajo acepta cortes. Es una decisión de política implícita.",
    },
]

for esc in escenarios:
    with st.expander(f"{esc['icon']} {esc['nombre']}"):
        st.markdown(f"""
        <span class="tag {esc['tag_color']}">{esc['tag']}</span>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**Descripción:** {esc['desc']}")
        st.markdown(f"**Qué cambia:** {esc['cambia']}")
        st.markdown(f"**Lección esperada:** {esc['leccion']}")
        
        st.button(f"▶️ Ejecutar escenario", disabled=True, key=esc['nombre'])

st.markdown("---")
st.info("🔜 **Semana 9** — Ejecución real de escenarios con resultados estandarizados: 1 gráfico + 3 bullets por escenario.")

# ── Explicación ───────────────────────────────────────────────────
section("¿Qué hace esta página?")

st.markdown("""
Esta página define **5 escenarios predefinidos** (presets) que el usuario activa con un clic:

1. Cada escenario cambia un conjunto específico de parámetros (costos, capacidades, VOLL).
2. Se re-ejecuta el despacho con esos parámetros.
3. Se muestran los resultados comparados con el caso base.
4. Cada escenario tiene una **lección clara** sobre el funcionamiento del sistema eléctrico.

El objetivo no es predecir el futuro, sino entender **cómo responde el sistema** a cambios en sus variables clave.
""")

footer()
