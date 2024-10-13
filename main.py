import streamlit as st
from data_processing import get_data
from visualization import create_map, create_bar_chart
from datetime import datetime, time

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Llamadas",
    layout="wide",  # Opciones: 'centered' o 'wide'
    initial_sidebar_state="expanded"  # Control del estado de la barra lateral
)

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

# Filtro de hora con un slider (rango de horas)
st.sidebar.markdown("### Filtro de hora")
start_hour = st.sidebar.slider(
    "Selecciona la hora de inicio",
    min_value=0,
    max_value=23,
    value=0,  # Hora de inicio por defecto
)

end_hour = st.sidebar.slider(
    "Selecciona la hora de fin",
    min_value=0,
    max_value=23,
    value=23,  # Hora de fin por defecto
)

# Crear las horas completas para el rango
start_time = time(start_hour, 0)  # Solo la hora completa
end_time = time(end_hour, 59)     # Termina al final de la hora
# Combinar fechas y horas seleccionadas
start_datetime = datetime.combine(start_date, start_time)
end_datetime = datetime.combine(end_date, end_time)

# Mostrar los valores seleccionados (opcional, para depuración)
st.write("Fecha y hora de inicio:", start_datetime)
st.write("Fecha y hora de fin:", end_datetime)

# Obtener los datos con el filtro de fechas y horas
df, geojson, color_var, title = get_data(opcion_analisis, start_datetime, end_datetime)

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
