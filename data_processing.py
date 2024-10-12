import pandas as pd
import json
from pymongo import MongoClient
import os
import streamlit as st

MONGODB_URI = st.secrets["MONGODB"]["URI"]
client = MongoClient(MONGODB_URI)
# Conexión a MongoDB
#client = MongoClient('mongodb://localhost:27017/')
#db = client['llamadas123']
#collection = db['llamadas2019']

def get_data(opcion_analisis, start_datetime, end_datetime):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['llamadas123']
    collection = db['llamadas2019']

    # Pipeline básico para contar incidentes filtrados por fecha y hora
    match_stage = {
        "$match": {
            "FECHA_INICIO_DESPLAZAMIENTO_MOVIL": {
                "$gte": start_datetime,
                "$lte": end_datetime
            }
        }
    }

    if opcion_analisis == "Número de Incidentes":
        pipeline = [
            match_stage,
            {
                "$group": {
                    "_id": "$LOCALIDAD",  # Agrupar por localidad
                    "INCIDENTES": { "$sum": 1 }  # Contar el número de incidentes
                }
            }
        ]
        df = pd.DataFrame(list(collection.aggregate(pipeline)))
        df.rename(columns={'_id': 'LOCALIDAD'}, inplace=True)
        color_var = "INCIDENTES"
        title = "Número de Incidentes por Localidad"

    elif opcion_analisis == "Prioridad":
        pipeline = [
            match_stage,
            {
                "$group": {
                    "_id": {"LOCALIDAD": "$LOCALIDAD", "PRIORIDAD": "$PRIORIDAD"},  # Agrupar por localidad y prioridad
                    "INCIDENTES": {"$sum": 1}
                }
            },
            {
                "$sort": {"_id.LOCALIDAD": 1, "INCIDENTES": -1}  # Ordenar por localidad
            }
        ]
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
