import pandas as pd
from datetime import datetime

# Load the CSV file into a pandas DataFrame
csv_file = "combined_file.csv"  # Replace with your actual file name
data = pd.read_csv(csv_file)

# Ensure correct date and time parsing
data["FECHA"] = pd.to_datetime(data[["Año", "Mes", "Dia"]])
data["HORA"] = pd.to_datetime(data["Hora"], format='%H').dt.hour

def get_filtered_data(start_date, end_date, start_hour, end_hour):
    # Filter data based on date and hour range
    filtered_data = data[
        (data["FECHA"] >= pd.Timestamp(start_date)) &
        (data["FECHA"] <= pd.Timestamp(end_date)) &
        (data["HORA"] >= start_hour) &
        (data["HORA"] <= end_hour)
    ]
    return filtered_data

def get_call_count_data(start_date, end_date, start_hour, end_hour):
    filtered_data = get_filtered_data(start_date, end_date, start_hour, end_hour)
    return filtered_data.groupby("LOCALIDAD").size().reset_index(name="count")

def get_avg_age_data(start_date, end_date, start_hour, end_hour):
    filtered_data = get_filtered_data(start_date, end_date, start_hour, end_hour)
    return filtered_data.groupby("LOCALIDAD")["EDAD"].mean().reset_index(name="avg_age")

def get_age_distribution(start_date, end_date, start_hour, end_hour):
    filtered_data = get_filtered_data(start_date, end_date, start_hour, end_hour)
    return filtered_data[["EDAD"]]

def get_incident_type_data(start_date, end_date, start_hour, end_hour):
    filtered_data = get_filtered_data(start_date, end_date, start_hour, end_hour)
    return filtered_data.groupby("TIPO_INCIDENTE").size().reset_index(name="count")

def get_gender_distribution(start_date, end_date, start_hour, end_hour):
    filtered_data = get_filtered_data(start_date, end_date, start_hour, end_hour)
    return filtered_data.groupby("GENERO").size().reset_index(name="count")

def get_incident_trend_data(start_date, end_date, start_hour, end_hour):
    filtered_data = get_filtered_data(start_date, end_date, start_hour, end_hour)
    filtered_data = filtered_data[filtered_data["TIPO_INCIDENTE"].isin(["Violencia Sexual", "Maltrato"])]
    trend_data = filtered_data.groupby(["Año", "TIPO_INCIDENTE"]).size().reset_index(name="count")
    return trend_data.rename(columns={"Año": "year", "TIPO_INCIDENTE": "incident_type"})
