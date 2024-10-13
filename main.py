import streamlit as st
from data_processing import get_data
from visualization import create_map, create_bar_chart
from datetime import datetime, time

# Configuración de la página
st.set_page_config(page_title="Análisis de Llamadas", layout="wide")

# Crear un título principal
st.title("Análisis de Llamadas de Emergencia")

# Crear un sidebar para seleccionar la variable a analizar
opcion_analisis = st.sidebar.selectbox(
    "Selecciona la variable a analizar:",
    ("Número de Incidentes", "Prioridad")
)

# Filtro de fecha (rango de fechas)
st.sidebar.markdown("### Filtro de fecha")
start_date = st.sidebar.date_input("Fecha de inicio", value=datetime(2019, 1, 1), min_value=datetime(2019, 1, 1), max_value=datetime(2023, 12, 31))
end_date = st.sidebar.date_input("Fecha de fin", value=datetime(2019, 12, 31), min_value=datetime(2019, 1, 1), max_value=datetime(2023, 12, 31))

# Filtros de hora
start_time = st.sidebar.time_input("Hora de inicio", value=time(0, 0))
end_time = st.sidebar.time_input("Hora de fin", value=time(23, 59))

# Llamada a la función get_data con fecha y hora por separado
df, geojson, color_var, title = get_data(opcion_analisis, start_date, end_date, start_time, end_time)

# Verificar si el DataFrame tiene datos
if df.empty:
    st.warning("No se encontraron datos para el rango de fechas y horas seleccionado.")
else:
    # Mostrar mapa o gráfico en función de la opción seleccionada
    if opcion_analisis == "Número de Incidentes":
        fig = create_map(df, geojson, color_var, title)
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = create_bar_chart(df, title)
        st.plotly_chart(fig, use_container_width=True)
