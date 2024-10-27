import streamlit as st
from data_processing import get_data
from visualization import create_map, create_bar_chart, create_treemap, create_histogram, create_choropleth_map
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
        df, geojson, color_var, title = get_data(opcion_analisis, year)

        # Crear el mapa coroplético
        choropleth_fig = create_choropleth_map(df, geojson, color_var, "Edad Promedio por Localidad")
        
        # Crear el histograma
        histogram_fig = create_histogram(df, title)
    
        # Mostrar el mapa coroplético
        st.plotly_chart(choropleth_fig)
    
        # Mostrar el histograma
        st.plotly_chart(histogram_fig)
