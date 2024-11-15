import streamlit as st
from datetime import datetime
import data_loader as dl
import visualizations as vz

# Page Setup
st.set_page_config(page_title="Bogotá Emergency Calls Dashboard", layout="wide")

# Sidebar with filters and page selection
st.sidebar.header("Filters and Navigation")

# Page navigation
page = st.sidebar.selectbox(
    "Choose a page",
    [
        "Número de llamadas",
        "Distribución y promedio de edad",
        "Distribución de tipo de incidentes",
        "Proporción de género",
        "Violencia sexual y maltrato"
    ]
)

# Date filter inputs
start_date = st.sidebar.date_input(
    'Start Date', datetime(2019, 1, 1), min_value=datetime(2019, 1, 1), max_value=datetime(2023, 12, 31)
)
end_date = st.sidebar.date_input(
    'End Date', datetime(2023, 12, 31), min_value=datetime(2019, 1, 1), max_value=datetime(2023, 12, 31)
)

# Hour range filter
start_hour = st.sidebar.slider('Start Hour', 0, 23, 0)
end_hour = st.sidebar.slider('End Hour', 0, 23, 23)

# Load data for all visualizations
df_call_count = dl.get_call_count_data(start_date, end_date, start_hour, end_hour)
df_avg_age = dl.get_avg_age_data(start_date, end_date, start_hour, end_hour)
df_age_distribution = dl.get_age_distribution(start_date, end_date, start_hour, end_hour)
df_incident_type = dl.get_incident_type_data(start_date, end_date, start_hour, end_hour)
df_gender_distribution = dl.get_gender_distribution(start_date, end_date, start_hour, end_hour)
df_incident_trend = dl.get_incident_trend_data(start_date, end_date, start_hour, end_hour)

# Render the selected page with the corresponding visualization
if page == "Número de llamadas":
    vz.plot_call_count_map(df_call_count)
elif page == "Distribución y promedio de edad":
    vz.plot_avg_age_map(df_avg_age)
    vz.plot_age_distribution(df_age_distribution)
elif page == "Distribución de tipo de incidentes":
    vz.plot_incident_type_distribution(df_incident_type)
elif page == "Proporción de género":
    vz.plot_gender_proportion(df_gender_distribution)
elif page == "Violencia sexual y maltrato":
    vz.plot_incident_trend(df_incident_trend)
