"""
Estilos compartidos para todas las páginas del simulador.
Importa esta función en cada página para mantener consistencia visual.
"""

import streamlit as st


def apply_styles():
    """Aplica el CSS personalizado del simulador."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');
        
        html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
        
        .page-header {
            background: linear-gradient(135deg, #0a1628 0%, #1a2742 50%, #0d2137 100%);
            border: 1px solid rgba(0, 212, 170, 0.15);
            border-radius: 16px;
            padding: 2rem 2.5rem;
            margin-bottom: 2rem;
        }
        .page-title {
            font-size: 2rem; font-weight: 700; color: #ffffff;
            margin: 0 0 0.3rem 0;
        }
        .page-subtitle {
            font-size: 0.95rem; color: #8899aa; margin: 0;
        }
        .accent { color: #00D4AA; }
        
        .card {
            background: linear-gradient(145deg, #141b2d, #1a2340);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;
        }
        .card-accent {
            background: linear-gradient(145deg, #141b2d, #1a2340);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;
            border-left: 3px solid #00D4AA;
        }
        .card h4 { color: #ffffff; margin: 0 0 0.5rem 0; }
        .card p, .card-accent p { color: #8899aa; margin: 0; font-size: 0.92rem; line-height: 1.6; }
        .card-accent h4 { color: #ffffff; margin: 0 0 0.5rem 0; }
        
        .section-title {
            font-size: 1.2rem; font-weight: 700; color: #ffffff;
            margin: 2rem 0 1rem 0; padding-bottom: 0.5rem;
            border-bottom: 2px solid rgba(0, 212, 170, 0.2);
        }
        
        .metric-row { display: flex; gap: 1rem; margin: 1rem 0; }
        .metric-card {
            background: linear-gradient(145deg, #141b2d, #1a2340);
            border: 1px solid rgba(0, 212, 170, 0.1);
            border-radius: 12px; padding: 1.2rem; flex: 1; text-align: center;
        }
        .metric-value { font-size: 1.5rem; font-weight: 700; color: #00D4AA; margin: 0; }
        .metric-label {
            font-size: 0.8rem; color: #667788; margin: 0.2rem 0 0 0;
            text-transform: uppercase; letter-spacing: 0.05em;
        }
        
        .tag {
            display: inline-block; padding: 0.3rem 0.8rem; border-radius: 15px;
            font-size: 0.8rem; font-weight: 500; margin: 0.2rem;
            font-family: 'JetBrains Mono', monospace;
        }
        .tag-green { background: rgba(0,212,170,0.12); color: #00D4AA; }
        .tag-blue { background: rgba(99,145,255,0.12); color: #6391FF; }
        .tag-orange { background: rgba(255,159,67,0.12); color: #FF9F43; }
        .tag-red { background: rgba(255,99,99,0.12); color: #FF6363; }
        .tag-gray { background: rgba(255,255,255,0.06); color: #667788; }
        
        .footer {
            text-align: center; color: #445566; font-size: 0.8rem;
            margin-top: 3rem; padding-top: 1rem;
            border-top: 1px solid rgba(255,255,255,0.05);
        }
        
        section[data-testid="stSidebar"] {
            background: #0a0f1a;
            border-right: 1px solid rgba(255,255,255,0.05);
        }
    </style>
    """, unsafe_allow_html=True)


def page_header(icon, title, subtitle):
    """Muestra el header estándar de cada página."""
    st.markdown(f"""
    <div class="page-header">
        <p class="page-title">{icon} {title}</p>
        <p class="page-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def section(title):
    """Muestra un título de sección."""
    st.markdown(f'<p class="section-title">{title}</p>', unsafe_allow_html=True)


def card(title, content):
    """Muestra una tarjeta informativa."""
    st.markdown(f"""
    <div class="card-accent">
        <h4>{title}</h4>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)


def footer():
    """Muestra el footer estándar."""
    st.markdown("""
    <div class="footer">
        Proyecto académico · Tec de Monterrey · Campus Santa Fe · 2025
    </div>
    """, unsafe_allow_html=True)
