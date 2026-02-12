"""
⚡ Simulador de Despacho Económico para México
Página principal — Home
"""

import streamlit as st

# ── Configuración ────────────────────────────────────────────────
st.set_page_config(
    page_title="Despacho Económico MX",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS personalizado ────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    
    .hero-container {
        background: linear-gradient(135deg, #0a1628 0%, #1a2742 50%, #0d2137 100%);
        border: 1px solid rgba(0, 212, 170, 0.15);
        border-radius: 16px;
        padding: 3rem 2.5rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%; right: -20%;
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(0,212,170,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-title {
        font-size: 2.8rem; font-weight: 700; color: #ffffff;
        margin: 0 0 0.3rem 0; letter-spacing: -0.02em;
    }
    .hero-accent { color: #00D4AA; }
    .hero-subtitle {
        font-size: 1.1rem; color: #8899aa; margin: 0;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .metric-row { display: flex; gap: 1rem; margin: 1.5rem 0; }
    .metric-card {
        background: linear-gradient(145deg, #141b2d, #1a2340);
        border: 1px solid rgba(0, 212, 170, 0.1);
        border-radius: 12px; padding: 1.3rem 1.5rem;
        flex: 1; text-align: center;
        transition: border-color 0.3s ease;
    }
    .metric-card:hover { border-color: rgba(0, 212, 170, 0.4); }
    .metric-value { font-size: 1.8rem; font-weight: 700; color: #00D4AA; margin: 0; }
    .metric-label {
        font-size: 0.85rem; color: #667788; margin: 0.3rem 0 0 0;
        text-transform: uppercase; letter-spacing: 0.05em;
    }
    
    .info-card {
        background: linear-gradient(145deg, #141b2d, #1a2340);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;
        border-left: 3px solid #00D4AA;
    }
    .info-card h4 { color: #ffffff; margin: 0 0 0.5rem 0; font-size: 1.05rem; }
    .info-card p { color: #8899aa; margin: 0; font-size: 0.92rem; line-height: 1.5; }
    
    .system-badge {
        display: inline-block; padding: 0.4rem 1rem; border-radius: 20px;
        font-size: 0.85rem; font-weight: 500; margin-right: 0.5rem;
        font-family: 'JetBrains Mono', monospace;
    }
    .badge-sin { background: rgba(0,212,170,0.12); color: #00D4AA; border: 1px solid rgba(0,212,170,0.25); }
    .badge-bca { background: rgba(99,145,255,0.12); color: #6391FF; border: 1px solid rgba(99,145,255,0.25); }
    .badge-bcs { background: rgba(255,159,67,0.12); color: #FF9F43; border: 1px solid rgba(255,159,67,0.25); }
    
    .section-header {
        font-size: 1.3rem; font-weight: 700; color: #ffffff;
        margin: 2rem 0 1rem 0; padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(0, 212, 170, 0.2);
    }
    
    .nav-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 1rem 0; }
    .nav-card {
        background: linear-gradient(145deg, #141b2d, #1a2340);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px; padding: 1.3rem;
        transition: all 0.3s ease;
    }
    .nav-card:hover { border-color: rgba(0,212,170,0.3); transform: translateY(-2px); }
    .nav-icon { font-size: 1.5rem; margin-bottom: 0.5rem; }
    .nav-title { font-size: 0.95rem; font-weight: 600; color: #ffffff; margin: 0 0 0.3rem 0; }
    .nav-desc { font-size: 0.8rem; color: #667788; margin: 0; }
    .nav-status { font-size: 0.75rem; margin-top: 0.5rem; padding: 0.2rem 0.6rem; border-radius: 10px; display: inline-block; }
    .status-done { background: rgba(0,212,170,0.12); color: #00D4AA; }
    .status-progress { background: rgba(255,159,67,0.12); color: #FF9F43; }
    .status-pending { background: rgba(255,255,255,0.06); color: #556677; }
    
    .footer {
        text-align: center; color: #445566; font-size: 0.8rem;
        margin-top: 3rem; padding-top: 1.5rem;
        border-top: 1px solid rgba(255,255,255,0.05);
    }
    
    section[data-testid="stSidebar"] {
        background: #0a0f1a;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚡ Despacho MX")
    st.caption("Simulador de despacho económico horario")
    st.markdown("---")
    st.markdown("""
    <div style="margin: 1rem 0;">
        <span class="system-badge badge-sin">SIN</span>
        <span class="system-badge badge-bca">BCA</span>
        <span class="system-badge badge-bcs">BCS</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    **Equipo**  
    María & Marifer · UX  
    Jime & Alexa · PyPSA  
    Regina & Musi · Data  
    Alexa · Team Lead
    """)
    st.markdown("---")
    st.caption("Tec de Monterrey · Santa Fe · 2025")

# ── Hero ─────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <p class="hero-title">⚡ Despacho <span class="hero-accent">Económico</span> MX</p>
    <p class="hero-subtitle">CENACE · PyPSA · Streamlit</p>
</div>
""", unsafe_allow_html=True)

# ── Métricas ─────────────────────────────────────────────────────
st.markdown("""
<div class="metric-row">
    <div class="metric-card">
        <p class="metric-value">3</p>
        <p class="metric-label">Sistemas Eléctricos</p>
    </div>
    <div class="metric-card">
        <p class="metric-value">7+</p>
        <p class="metric-label">Tecnologías</p>
    </div>
    <div class="metric-card">
        <p class="metric-value">5</p>
        <p class="metric-label">Escenarios</p>
    </div>
    <div class="metric-card">
        <p class="metric-value">24h</p>
        <p class="metric-label">Resolución Horaria</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Qué es ───────────────────────────────────────────────────────
st.markdown('<p class="section-header">¿Qué es este simulador?</p>', unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
    <h4>Simulador de despacho económico horario para México</h4>
    <p>
        Modela cómo se asigna la generación eléctrica hora por hora 
        en los tres sistemas aislados de México: <strong>SIN</strong> (Sistema Interconectado Nacional), 
        <strong>BCA</strong> (Baja California) y <strong>BCS</strong> (Baja California Sur). 
        Usa datos reales de demanda de CENACE y optimización con PyPSA para encontrar 
        el despacho de mínimo costo.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="info-card">
        <h4>📊 Datos reales</h4>
        <p>Demanda horaria de CENACE con batching, caché y validación de calidad.</p>
    </div>
    <div class="info-card">
        <h4>🎛️ Interactivo</h4>
        <p>Ajusta costos marginales con sliders y observa cambios en tiempo real.</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="info-card">
        <h4>🔧 Optimización real</h4>
        <p>PyPSA + HiGHS para resolver el despacho como optimización lineal.</p>
    </div>
    <div class="info-card">
        <h4>📈 5 escenarios</h4>
        <p>Fuel shock, renewables boom, outage, storage y scarcity knob.</p>
    </div>
    """, unsafe_allow_html=True)

# ── Navegación ───────────────────────────────────────────────────
st.markdown('<p class="section-header">Secciones del simulador</p>', unsafe_allow_html=True)

st.markdown("""
<div class="nav-grid">
    <div class="nav-card">
        <div class="nav-icon">📊</div>
        <p class="nav-title">Demanda CENACE</p>
        <p class="nav-desc">Descarga y visualización de demanda horaria real.</p>
        <span class="nav-status status-progress">Semana 2</span>
    </div>
    <div class="nav-card">
        <div class="nav-icon">🏭</div>
        <p class="nav-title">Capacidades</p>
        <p class="nav-desc">Capacidad instalada por tecnología (2024 y 2026).</p>
        <span class="nav-status status-pending">Semana 3</span>
    </div>
    <div class="nav-card">
        <div class="nav-icon">🔧</div>
        <p class="nav-title">Despacho</p>
        <p class="nav-desc">Optimización PyPSA: generación, curtailment, shedding.</p>
        <span class="nav-status status-pending">Semana 4</span>
    </div>
    <div class="nav-card">
        <div class="nav-icon">🎛️</div>
        <p class="nav-title">Sensibilidad</p>
        <p class="nav-desc">Sliders de costos marginales con análisis de impacto.</p>
        <span class="nav-status status-pending">Semana 6</span>
    </div>
    <div class="nav-card">
        <div class="nav-icon">📈</div>
        <p class="nav-title">Escenarios</p>
        <p class="nav-desc">5 presets con lecciones del sistema eléctrico.</p>
        <span class="nav-status status-pending">Semana 9</span>
    </div>
    <div class="nav-card">
        <div class="nav-icon">📖</div>
        <p class="nav-title">Metodología</p>
        <p class="nav-desc">Supuestos, limitaciones, fuentes y docs.</p>
        <span class="nav-status status-done">✓ Listo</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Proyecto académico · Tec de Monterrey · Campus Santa Fe · 2025<br>
    Este simulador no pretende replicar el despacho real de CENACE
</div>
""", unsafe_allow_html=True)
