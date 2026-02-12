# ⚡ Simulador de Despacho Económico — México

Simulador online de despacho económico horario para los tres sistemas eléctricos aislados de México (SIN, BCA, BCS) usando datos reales de CENACE y PyPSA.

## Setup rápido

```bash
# 1. Clonar el repo
git clone <URL_DEL_REPO>
cd simulador-despacho

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Correr la app
streamlit run app.py
```

## Estructura

```
├── app.py                    # Página principal
├── pages/
│   ├── 1_📊_Demanda.py      # Demanda CENACE
│   ├── 2_⚡_Capacidades.py   # Capacidad instalada
│   ├── 3_🔧_Despacho.py     # Resultados optimización
│   ├── 4_💰_Sensibilidad.py  # Sliders de costos
│   ├── 5_🎯_Escenarios.py   # 5 presets
│   └── 6_📖_Metodologia.py  # Docs y limitaciones
├── requirements.txt
└── README.md
```

## Stack

- **Python** — Lenguaje único
- **Streamlit** — UI interactiva
- **PyPSA** — Optimización de despacho (solver HiGHS)
- **CENACE** — Datos de demanda reales
- **Plotly** — Visualizaciones

## Equipo

| Nombre | Rol |
|--------|-----|
| TBD | Project Leader |
| TBD | Data Pipeline |
| TBD | Modelo PyPSA |
| TBD | Frontend/UX |
| TBD | TBD |
| TBD | TBD |

## Licencia

Proyecto académico — Tecnológico de Monterrey, 2025.
