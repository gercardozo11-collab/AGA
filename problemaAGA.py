import streamlit as st
from scipy.optimize import linprog

st.set_page_config(page_title="Optimizador de Sensores")

st.title("Optimizador de Sensores")

st.subheader("Cobertura por sensor")
c1 = st.number_input("Temperatura", value=1)
c2 = st.number_input("Presión", value=2)
c3 = st.number_input("Vibración", value=3)
c4 = st.number_input("Corriente", value=1)

st.subheader("Capacidad máxima de recursos")

max_canales = st.number_input("Canales de adquisición", value=80)
max_banda = st.number_input("Ancho de banda (Mbps)", value=150)
max_potencia = st.number_input("Potencia (W)", value=100)
max_memoria = st.number_input("Memoria (GB/día)", value=180)

st.subheader("Restricciones adicionales")

min_x1 = st.number_input(
    "Mínimo sensores de temperatura",
    value=10
)

min_x2 = st.number_input(
    "Mínimo sensores de presión",
    value=15
)

max_x3 = st.number_input(
    "Máximo sensores de vibración",
    value=20
)

if st.button("Resolver"):

    c = [-c1, -c2, -c3, -c4]

    A = [
        [1, 2, 2, 1],
        [2, 3, 4, 2],
        [1, 2, 3, 2],
        [3, 4, 5, 2]
    ]

    b = [
        max_canales,
        max_banda,
        max_potencia,
        max_memoria
    ]

    bounds = [
        (min_x1, None),
        (min_x2, None),
        (0, max_x3),
        (0, None)
    ]

    resultado = linprog(
        c,
        A_ub=A,
        b_ub=b,
        bounds=bounds,
        method="highs"
    )

    if resultado.success:

        x1, x2, x3, x4 = resultado.x

        st.success("Solución encontrada")

        st.metric(
            "Cobertura máxima",
            round(-resultado.fun, 2)
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Sensores temperatura",
                round(x1, 2)
            )

            st.metric(
                "Sensores presión",
                round(x2, 2)
            )

        with col2:
            st.metric(
                "Sensores vibración",
                round(x3, 2)
            )

            st.metric(
                "Sensores corriente",
                round(x4, 2)
            )

    else:
        st.error(
            "No existe una solución factible con esos parámetros."
        )
