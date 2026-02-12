# ⚡ Simulador de Despacho Económico para México

Simulador de despacho económico horario para los tres sistemas eléctricos aislados de México (SIN, BCA, BCS) usando datos reales de CENACE y optimización con PyPSA.

## 🚀 Cómo correr la aplicación

### Requisitos
- Python 3.10 o superior
- pip

### Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU-USUARIO/simulador-despacho.git
cd simulador-despacho

# 2. Crear entorno virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # En Mac/Linux
# venv\Scripts\activate   # En Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la app
streamlit run app.py
```

La app se abrirá en `http://localhost:8501`.

## 📂 Estructura del proyecto

```
simulador-despacho/
├── app.py                          # Página principal
├── pages/
│   ├── 1_📊_Demanda_CENACE.py     # Descarga y visualización de demanda
│   ├── 2_🏭_Capacidades.py        # Capacidad instalada por tecnología
│   ├── 3_🔧_Despacho.py           # Modelo PyPSA y resultados
│   ├── 4_🎛️_Sensibilidad.py       # Sliders de costos
│   ├── 5_📈_Escenarios.py         # 5 presets predefinidos
│   └── 6_📖_Metodología.py        # Documentación y limitaciones
├── requirements.txt
└── README.md
```

## 🏗️ Sistemas modelados

| Sistema | Descripción | Cobertura |
|---------|------------|-----------|
| SIN | Sistema Interconectado Nacional | ~95% de México |
| BCA | Baja California | Norte de BC |
| BCS | Baja California Sur | Sur de BC |

## 🛠️ Stack tecnológico

- **Python** — Lenguaje único
- **Streamlit** — Interfaz web interactiva
- **PyPSA** ≥ 0.26 — Optimización de despacho
- **HiGHS** — Solver (incluido con Linopy)
- **Plotly** — Visualizaciones
- **CENACE API** — Datos de demanda horaria real

## ⚠️ Limitaciones

Este simulador es un proyecto académico y **no** replica el despacho real de CENACE. No modela: red interna, interconexiones, unit commitment, reservas, restricciones N-1, ni costos reales por planta.

## 👥 Equipo

Tec de Monterrey · Campus Santa Fe · 2025
