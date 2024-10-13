import streamlit as st
from data_processing import get_data
from visualization import create_map, create_bar_chart
from datetime import datetime, time

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Llamadas",
    layout="wide",  
    initial_sidebar_state="expanded"
)

# Crear un título principal
st.title("Análisis de Llamadas de Emergencia")

# Crear un sidebar para seleccionar la variable a analizar
opcion_analisis = st.sidebar.selectbox(
    "Selecciona la variable a analizar:",
    ("Número de Incidentes", "Prioridad")
)

# Filtro de fecha (rango de fechas) y utilizamos el año para cambiar de colección
st.sidebar.markdown("### Filtro de fecha")
start_date = st.sidebar.date_input("Fecha de inicio", value=datetime(2019, 1, 1))
end_date = st.sidebar.date_input("Fecha de fin", value=datetime(2019, 12, 31))

# Filtro de hora con un slider (rango de horas)
st.sidebar.markdown("### Filtro de hora")
start_time, end_time = st.sidebar.slider(
    "Selecciona el rango de horas",
    value=(time(0, 0), time(23, 59)),
    format="HH:mm"
)

# Obtener el año del rango de fechas seleccionado para cambiar de colección
start_year = start_date.year
end_year = end_date.year

# Obtener los datos de la colección según el año y el filtro de fechas/horas
df, geojson, color_var, title = get_data(opcion_analisis, start_year, start_date, end_date, start_time, end_time)

# Verificar si el DataFrame tiene datos
if df.empty:
    st.warning("No se encontraron datos para el rango de fechas y horas seleccionado.")
else:
    # Mostrar mapa o gráfico en función de la opción seleccionada
    if opcion_analisis == "Número de Incidentes":
        fig = create_map(df, geojson, color_var, title)
        st.plotly_chart(fig, use_container_width=True)  # Asegurarse de que el gráfico use todo el ancho
    else:
        fig = create_bar_chart(df, title)
        st.plotly_chart(fig, use_container_width=True)  # Asegurarse de que el gráfico use todo el ancho
