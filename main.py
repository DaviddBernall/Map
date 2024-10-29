import streamlit as st
from data_processing import get_data
from visualization import create_map, create_bar_chart, create_treemap, create_histogram
from datetime import datetime, time

# Configuración de la página
st.set_page_config(page_title="Análisis de Llamadas", layout="wide")

# Crear un título principal
st.title("Análisis de Llamadas de Emergencia")

# Crear un sidebar para seleccionar la variable a analizar
opcion_analisis = st.sidebar.selectbox(
    "Selecciona la variable a analizar:",
    ("Número de Incidentes", "Prioridad", "Tipo de Incidente","Edad")
)

# Filtro de año
st.sidebar.markdown("### Selecciona el año")
year = st.sidebar.selectbox("Año", options=[2019, 2020, 2021, 2022, 2023])

# Obtener los datos
df, geojson, color_var, title = get_data(opcion_analisis, year)

# Verificar si el DataFrame tiene datos
if df.empty:
    st.warning("No se encontraron datos para el año seleccionado.")
else:
    # Mostrar el gráfico en función de la opción seleccionada
    if opcion_analisis == "Número de Incidentes":
        fig = create_map(df, geojson, color_var, title)
        st.plotly_chart(fig, use_container_width=True)
    elif opcion_analisis == "Prioridad":
        fig = create_bar_chart(df, title)
        st.plotly_chart(fig, use_container_width=True)
    elif opcion_analisis == "Tipo de Incidente":
        fig = create_treemap(df, "Distribución de Incidentes por Tipo")
        st.plotly_chart(fig, use_container_width=True)
    elif opcion_analisis == "Edad":
    df = df.dropna(subset=['EDAD'])  # Eliminar filas donde 'EDAD' es NaN
    if df.empty:
        st.warning("No se encontraron datos de edad para el año seleccionado.")
    else:
        # Mostrar el histograma
        fig_hist = create_histogram(df, title)
        st.plotly_chart(fig_hist, use_container_width=True)

        # Crear el mapa coroplético
        fig_map = create_map(df, geojson, color_var, title)
        st.plotly_chart(fig_map, use_container_width=True)
