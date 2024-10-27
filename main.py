import streamlit as st
from data_processing import get_data
from visualization import create_map, create_bar_chart, create_treemap
from datetime import datetime, time

# Configuración de la página
st.set_page_config(page_title="Análisis de Llamadas", layout="wide")

# Crear un título principal
st.title("Análisis de Llamadas de Emergencia")

# Crear un sidebar para seleccionar la variable a analizar
opcion_analisis = st.sidebar.selectbox(
    "Selecciona la variable a analizar:",
    ("Número de Incidentes", "Prioridad", "Tipo de Incidente")
)

# Filtro de fecha (rango de fechas)
st.sidebar.markdown("### Filtro de fecha")
start_date = st.sidebar.date_input("Fecha de inicio", value=datetime(2019, 1, 1), min_value=datetime(2019, 1, 1), max_value=datetime(2023, 12, 31))
end_date = st.sidebar.date_input("Fecha de fin", value=datetime(2019, 12, 31), min_value=datetime(2019, 1, 1), max_value=datetime(2023, 12, 31))

# Filtro de hora
st.sidebar.markdown("### Filtro de hora")
start_time, end_time = st.sidebar.slider(
    "Selecciona el rango de horas",
    value=(time(0, 0), time(23, 59)),
    format="HH:mm"
)

# Combinar fechas y horas seleccionadas
start_datetime = datetime.combine(start_date, start_time)
end_datetime = datetime.combine(end_date, end_time)

# Obtener los datos
df, geojson, color_var, title = get_data(opcion_analisis, start_datetime, end_datetime)

# Verificar si el DataFrame tiene datos
if df.empty:
    st.warning("No se encontraron datos para el rango de fechas y horas seleccionado.")
else:
    # Mostrar mapa, gráfico de barras, o treemap en función de la opción seleccionada
    if opcion_analisis == "Número de Incidentes":
        fig = create_map(df, geojson, color_var, title)
        st.plotly_chart(fig, use_container_width=True)
    elif opcion_analisis == "Prioridad":
        fig = create_bar_chart(df, title)
        st.plotly_chart(fig, use_container_width=True)
    elif opcion_analisis == "Tipo de Incidente":
        fig = create_treemap(df, "Distribución de Incidentes por Tipo")
        st.plotly_chart(fig, use_container_width=True)
