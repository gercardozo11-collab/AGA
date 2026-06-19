import streamlit as st
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

st.set_page_config(
    page_title="Optimizador de Sensores",
    page_icon="📡",
    layout="centered"
)

st.title("📡 Optimizador de Sensores")

# =========================
# COBERTURA
# =========================

st.subheader("Cobertura aportada por cada sensor")

c1 = st.number_input(
    "Temperatura",
    min_value=0,
    value=1,
    step=1,
    format="%d"
)

c2 = st.number_input(
    "Presión",
    min_value=0,
    value=2,
    step=1,
    format="%d"
)

c3 = st.number_input(
    "Vibración",
    min_value=0,
    value=3,
    step=1,
    format="%d"
)

c4 = st.number_input(
    "Corriente",
    min_value=0,
    value=1,
    step=1,
    format="%d"
)

# =========================
# RECURSOS
# =========================

st.subheader("Capacidades máximas")

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

# =========================
# RESTRICCIONES
# =========================

st.subheader("Restricciones")

min_x1 = st.number_input(
    "Mínimo sensores de temperatura",
    min_value=0,
    value=10,
    step=1,
    format="%d"
)

min_x2 = st.number_input(
    "Mínimo sensores de presión",
    min_value=0,
    value=15,
    step=1,
    format="%d"
)

max_x3 = st.number_input(
    "Máximo sensores de vibración",
    min_value=0,
    value=20,
    step=1,
    format="%d"
)

# =========================
# RESOLVER
# =========================

if st.button("Resolver"):

    # Maximizar -> minimizar negativo
    c = -np.array([c1, c2, c3, c4])

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

    limites = Bounds(
        [min_x1, min_x2, 0, 0],
        [np.inf, np.inf, max_x3, np.inf]
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

        st.success("Solución encontrada")

        st.subheader("Resultado")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Temperatura", x1)
            st.metric("Presión", x2)

        with col2:
            st.metric("Vibración", x3)
            st.metric("Corriente", x4)

        st.metric("Cobertura máxima", cobertura)

    else:
        st.error(
            "No existe una solución factible con los parámetros ingresados."
        )
