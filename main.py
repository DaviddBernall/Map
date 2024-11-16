import streamlit as st
from data import get_data, db
from visualization import create_map, create_bar_chart, create_treemap, create_histogram, create_segmented_bar_chart
from datetime import datetime, time
from data import get_aggregated_data_by_incident_and_gender  # Importa la función

# Configuración de la página
st.set_page_config(page_title="Análisis de Llamadas de Emergencias", layout="wide")  # Layout centrado para dispositivos móviles

# Crear un sidebar para seleccionar la variable a analizar
opcion_analisis = st.sidebar.selectbox(
    "Selecciona la variable a analizar:",
    ("Número de Incidentes", "Prioridad", "Tipo de Incidente","Edad por Localidad","Violencia sexual y maltrato por localidad",
     "Violencia y género por año")
)

if opcion_analisis == "Violencia y género por año":
    # Trabajar con todas las colecciones por año
    years = [2019, 2020, 2021, 2022, 2023]  # Lista de años

    # Obtener los datos agregados
    df = get_aggregated_data_by_incident_and_gender(years, db)

    if df.empty:
        st.warning("No se encontraron datos para los años seleccionados.")
    else:
        # Crear gráfico de barras segmentadas
        fig = create_segmented_bar_chart(df, "Distribución de Violencia y Género por Año")
        st.plotly_chart(fig, use_container_width=True)

else:
    # Para las otras opciones
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
            fig = create_map(df, geojson, color_var, title, "Reds")
            st.plotly_chart(fig, use_container_width=True)
        elif opcion_analisis == "Prioridad":
            fig = create_bar_chart(df, title)
            st.plotly_chart(fig, use_container_width=True)
        elif opcion_analisis == "Tipo de Incidente":
            fig = create_treemap(df, "Distribución de Incidentes por Tipo")
            st.plotly_chart(fig, use_container_width=True)
        elif opcion_analisis == "Edad por Localidad":
            fig = create_map(df, geojson, color_var, title,"Viridis")
            st.plotly_chart(fig, use_container_width=True)
        elif opcion_analisis == "Violencia sexual y maltrato por localidad":
            fig = create_map(df, geojson, color_var, title, "Reds")
            st.plotly_chart(fig, use_container_width=True) 
