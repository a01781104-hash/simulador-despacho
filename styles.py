"""
Estilos compartidos para todas las páginas del simulador.
Tema claro profesional.
"""

import streamlit as st


def apply_styles():
    """Aplica el CSS personalizado del simulador (tema claro)."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');
        
        html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
        
        .page-header {
            background: linear-gradient(135deg, #f0faf6 0%, #e6f7f1 50%, #eef9f5 100%);
            border: 1px solid rgba(0, 153, 122, 0.15);
            border-radius: 16px;
            padding: 2rem 2.5rem;
            margin-bottom: 2rem;
        }
        .page-title {
            font-size: 2rem; font-weight: 700; color: #1a1a2e;
            margin: 0 0 0.3rem 0;
        }
        .page-subtitle {
            font-size: 0.95rem; color: #667788; margin: 0;
        }
        .accent { color: #00997A; }
        
        .card {
            background: #ffffff;
            border: 1px solid #e8ecf0;
            border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }
        .card-accent {
            background: #ffffff;
            border: 1px solid #e8ecf0;
            border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;
            border-left: 3px solid #00997A;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }
        .card h4, .card-accent h4 { color: #1a1a2e; margin: 0 0 0.5rem 0; }
        .card p, .card-accent p { color: #556677; margin: 0; font-size: 0.92rem; line-height: 1.6; }
        
        .section-title {
            font-size: 1.2rem; font-weight: 700; color: #1a1a2e;
            margin: 2rem 0 1rem 0; padding-bottom: 0.5rem;
            border-bottom: 2px solid rgba(0, 153, 122, 0.2);
        }
        
        .metric-row { display: flex; gap: 1rem; margin: 1rem 0; }
        .metric-card {
            background: #ffffff;
            border: 1px solid rgba(0, 153, 122, 0.15);
            border-radius: 12px; padding: 1.2rem; flex: 1; text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            transition: border-color 0.3s ease;
        }
        .metric-card:hover { border-color: rgba(0, 153, 122, 0.4); }
        .metric-value { font-size: 1.5rem; font-weight: 700; color: #00997A; margin: 0; }
        .metric-label {
            font-size: 0.8rem; color: #889099; margin: 0.2rem 0 0 0;
            text-transform: uppercase; letter-spacing: 0.05em;
        }
        
        .tag {
            display: inline-block; padding: 0.3rem 0.8rem; border-radius: 15px;
            font-size: 0.8rem; font-weight: 500; margin: 0.2rem;
            font-family: 'JetBrains Mono', monospace;
        }
        .tag-green { background: rgba(0,153,122,0.1); color: #00997A; }
        .tag-blue { background: rgba(59,105,199,0.1); color: #3B69C7; }
        .tag-orange { background: rgba(219,132,40,0.1); color: #DB8428; }
        .tag-red { background: rgba(199,59,59,0.1); color: #C73B3B; }
        .tag-gray { background: rgba(100,110,120,0.1); color: #646E78; }
        
        .footer {
            text-align: center; color: #99aabb; font-size: 0.8rem;
            margin-top: 3rem; padding-top: 1rem;
            border-top: 1px solid #e8ecf0;
        }
        
        section[data-testid="stSidebar"] {
            background: #F7F9FB;
            border-right: 1px solid #e8ecf0;
        }
    </style>
    """, unsafe_allow_html=True)


def page_header(icon, title, subtitle):
    st.markdown(f"""
    <div class="page-header">
        <p class="page-title">{icon} {title}</p>
        <p class="page-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def section(title):
    st.markdown(f'<p class="section-title">{title}</p>', unsafe_allow_html=True)


def card(title, content):
    st.markdown(f"""
    <div class="card-accent">
        <h4>{title}</h4>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)


def footer():
    st.markdown("""
    <div class="footer">
        Proyecto académico · Tec de Monterrey · Campus Santa Fe · 2025
    </div>
    """, unsafe_allow_html=True)
