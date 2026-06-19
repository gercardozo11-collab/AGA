import streamlit as st
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

st.set_page_config(
    page_title="Optimizador de Sensores",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Optimizador de Sensores")

# ==================================================
# COBERTURA
# ==================================================

st.subheader("Cobertura aportada por cada sensor")

col1, col2, col3, col4 = st.columns(4)

with col1:
    c1 = st.number_input(
        "Temperatura",
        min_value=0,
        value=1,
        step=1,
        format="%d"
    )

with col2:
    c2 = st.number_input(
        "Presión",
        min_value=0,
        value=2,
        step=1,
        format="%d"
    )

with col3:
    c3 = st.number_input(
        "Vibración",
        min_value=0,
        value=3,
        step=1,
        format="%d"
    )

with col4:
    c4 = st.number_input(
        "Corriente",
        min_value=0,
        value=1,
        step=1,
        format="%d"
    )

# ==================================================
# RECURSOS
# ==================================================

st.subheader("Capacidades máximas del sistema")

col1, col2 = st.columns(2)

with col1:
    max_canales = st.number_input(
        "Canales de adquisición",
        min_value=1,
        value=80,
        step=1,
        format="%d"
    )

    max_banda = st.number_input(
        "Ancho de banda (Mbps)",
        min_value=1,
        value=150,
        step=1,
        format="%d"
    )

with col2:
    max_potencia = st.number_input(
        "Potencia (W)",
        min_value=1,
        value=100,
        step=1,
        format="%d"
    )

    max_memoria = st.number_input(
        "Memoria (GB/día)",
        min_value=1,
        value=180,
        step=1,
        format="%d"
    )

# ==================================================
# RESTRICCIONES
# ==================================================

st.subheader("Cantidad de sensores a instalar")

fila1_col1, fila1_col2 = st.columns(2)

with fila1_col1:
    st.markdown("### 🌡️ Temperatura")

    min_x1 = st.number_input(
        "Mínimo temperatura",
        min_value=0,
        value=10,
        step=1,
        format="%d"
    )

    max_x1 = st.number_input(
        "Máximo temperatura",
        min_value=min_x1,
        value=100,
        step=1,
        format="%d"
    )

with fila1_col2:
    st.markdown("### 🔧 Presión")

    min_x2 = st.number_input(
        "Mínimo presión",
        min_value=0,
        value=15,
        step=1,
        format="%d"
    )

    max_x2 = st.number_input(
        "Máximo presión",
        min_value=min_x2,
        value=100,
        step=1,
        format="%d"
    )

fila2_col1, fila2_col2 = st.columns(2)

with fila2_col1:
    st.markdown("### 📳 Vibración")

    min_x3 = st.number_input(
        "Mínimo vibración",
        min_value=0,
        value=0,
        step=1,
        format="%d"
    )

    max_x3 = st.number_input(
        "Máximo vibración",
        min_value=min_x3,
        value=20,
        step=1,
        format="%d"
    )

with fila2_col2:
    st.markdown("### ⚡ Corriente")

    min_x4 = st.number_input(
        "Mínimo corriente",
        min_value=0,
        value=0,
        step=1,
        format="%d"
    )

    max_x4 = st.number_input(
        "Máximo corriente",
        min_value=min_x4,
        value=50,
        step=1,
        format="%d"
    )

# ==================================================
# RESOLVER
# ==================================================

if st.button("🚀 Resolver"):

    # Función objetivo (negativa porque MILP minimiza)
    c = -np.array([c1, c2, c3, c4])

    # Restricciones de recursos
    restricciones = LinearConstraint(
        [
            [1, 2, 2, 1],  # canales
            [2, 3, 4, 2],  # banda
            [1, 2, 3, 2],  # potencia
            [3, 4, 5, 2]   # memoria
        ],
        -np.inf,
        [
            max_canales,
            max_banda,
            max_potencia,
            max_memoria
        ]
    )

    # Límites mínimo y máximo de cada sensor
    limites = Bounds(
        [min_x1, min_x2, min_x3, min_x4],
        [max_x1, max_x2, max_x3, max_x4]
    )

    # Todas las variables enteras
    integrality = np.ones(4)

    resultado = milp(
        c=c,
        constraints=restricciones,
        bounds=limites,
        integrality=integrality
    )

    if resultado.success:

        x1, x2, x3, x4 = map(int, np.round(resultado.x))
        cobertura = int(round(-resultado.fun))

        st.success("Solución óptima encontrada")

        st.subheader("Resultado")

        r1, r2, r3, r4 = st.columns(4)

        with r1:
            st.metric("🌡️ Temperatura", x1)

        with r2:
            st.metric("🔧 Presión", x2)

        with r3:
            st.metric("📳 Vibración", x3)

        with r4:
            st.metric("⚡ Corriente", x4)

        st.metric(
            "📈 Cobertura máxima",
            cobertura
        )

    else:
        st.error(
            "No existe una solución factible con los parámetros ingresados."
        )
