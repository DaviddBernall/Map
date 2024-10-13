import pandas as pd
import json
from pymongo import MongoClient
import streamlit as st
from datetime import datetime

# Conexión a MongoDB desde los Secrets de Streamlit
MONGODB_URI = st.secrets["MONGODB"]["URI"]
client = MongoClient(MONGODB_URI)
db = client['Llamadas123']  # Base de datos de llamadas

def get_data(opcion_analisis, start_datetime, end_datetime):
    # Determinar la colección a usar según el año de start_datetime
    year = start_datetime.year
    if year == 2019:
        collection_name = "llamadas2019"
    elif year == 2020:
        collection_name = "llamadas2020"
    elif year == 2021:
        collection_name = "llamadas2021"
    elif year == 2022:
        collection_name = "llamadas2022"
    elif year == 2023:
        collection_name = "llamadas2023"
    else:
        raise ValueError("Año fuera de rango")

    # Acceder a la colección correspondiente
    collection = db[collection_name]

    # Separar las fechas y horas en el filtro
    start_date_str = start_datetime.strftime("%d/%m/%Y")
    end_date_str = end_datetime.strftime("%d/%m/%Y")
    start_time_str = start_datetime.strftime("%H:%M:%S")
    end_time_str = end_datetime.strftime("%H:%M:%S")

    # Pipeline para filtrar por fecha y hora
    pipeline = [
        {
            "$match": {
                "FECHA_INICIO_DESPLAZAMIENTO_MOVIL": {
                    "$gte": start_date_str,
                    "$lte": end_date_str
                },
                "HORA_INICIO_DESPLAZAMIENTO_MOVIL": {
                    "$gte": start_time_str,
                    "$lte": end_time_str
                }
            }
        }
    ]

    # Pipeline para agrupar por opción seleccionada
    if opcion_analisis == "Número de Incidentes":
        pipeline.append(
            {
                "$group": {
                    "_id": "$LOCALIDAD",  # Agrupar por localidad
                    "INCIDENTES": {"$sum": 1}  # Contar el número de incidentes
                }
            }
        )
        df = pd.DataFrame(list(collection.aggregate(pipeline)))
        df.rename(columns={'_id': 'LOCALIDAD'}, inplace=True)
        color_var = "INCIDENTES"
        title = "Número de Incidentes por Localidad"

    elif opcion_analisis == "Prioridad":
        pipeline.append(
            {
                "$group": {
                    "_id": {"LOCALIDAD": "$LOCALIDAD", "PRIORIDAD": "$PRIORIDAD"},  # Agrupar por localidad y prioridad
                    "INCIDENTES": {"$sum": 1}
                }
            }
        )
        df = pd.DataFrame(list(collection.aggregate(pipeline)))
        df['LOCALIDAD'] = df['_id'].apply(lambda x: x['LOCALIDAD'])
        df['PRIORIDAD'] = df['_id'].apply(lambda x: x['PRIORIDAD'])
        df.drop(columns=['_id'], inplace=True)
        color_var = None
        title = "Incidentes por Prioridad y Localidad"

    # Cargar el archivo GeoJSON (puede estar predefinido en el proyecto)
    with open("localidades.geojson") as f:
        geojson = json.load(f)

    return df, geojson, color_var, title
