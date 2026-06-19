import streamlit as st

st.set_page_config(
    page_title="Optimización de Sensores",
    page_icon="📡",
    layout="centered"
)

st.title("📡 Diseño de Red de Sensores")
st.subheader("Maximización de la cobertura de monitoreo")

st.markdown("""
### Función objetivo

Maximizar:

**Z = x₁ + 2x₂ + 3x₃ + x₄**

### Restricciones

**Canales de adquisición**

x₁ + 2x₂ + 2x₃ + x₄ ≤ 80

**Ancho de banda**

2x₁ + 3x₂ + 4x₃ + 2x₄ ≤ 150

**Potencia**

x₁ + 2x₂ + 3x₃ + 2x₄ ≤ 100

**Memoria**

3x₁ + 4x₂ + 5x₃ + 2x₄ ≤ 180

**Condiciones adicionales**

- x₁ ≥ 10
- x₂ ≥ 15
- x₃ ≤ 20
- x₁, x₂, x₃, x₄ ≥ 0
""")

def cumple(x1, x2, x3, x4):
    return (
        x1 + 2*x2 + 2*x3 + x4 <= 80 and
        2*x1 + 3*x2 + 4*x3 + 2*x4 <= 150 and
        x1 + 2*x2 + 3*x3 + 2*x4 <= 100 and
        3*x1 + 4*x2 + 5*x3 + 2*x4 <= 180 and
        x1 >= 10 and
        x2 >= 15 and
        x3 <= 20 and
        x4 >= 0
    )

if st.button("🔍 Resolver problema"):

    mejor_z = -1
    mejor_solucion = None

    progress = st.progress(0)

    total_x1 = 71
    actual = 0

    for x1 in range(10, 81):

        actual += 1
        progress.progress(actual / total_x1)

        for x2 in range(15, 81):
            for x3 in range(0, 21):
                for x4 in range(0, 81):

                    if cumple(x1, x2, x3, x4):

                        z = x1 + 2*x2 + 3*x3 + x4

                        if z > mejor_z:
                            mejor_z = z
                            mejor_solucion = (x1, x2, x3, x4)

    progress.empty()

    if mejor_solucion:

        x1, x2, x3, x4 = mejor_solucion

        st.success("Solución óptima encontrada")

        st.markdown("## Resultados")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Temperatura (x₁)", x1)
            st.metric("Presión (x₂)", x2)

        with col2:
            st.metric("Vibración (x₃)", x3)
            st.metric("Corriente (x₄)", x4)

        st.metric("Cobertura máxima Z", mejor_z)

        canales = x1 + 2*x2 + 2*x3 + x4
        banda = 2*x1 + 3*x2 + 4*x3 + 2*x4
        potencia = x1 + 2*x2 + 3*x3 + 2*x4
        memoria = 3*x1 + 4*x2 + 5*x3 + 2*x4

        st.markdown("## Uso de recursos")

        st.write(f"📶 Canales: **{canales}/80**")
        st.write(f"🌐 Ancho de banda: **{banda}/150 Mbps**")
        st.write(f"⚡ Potencia: **{potencia}/100 W**")
        st.write(f"💾 Memoria: **{memoria}/180 GB/día**")

    else:
        st.error("No se encontró una solución factible.")
