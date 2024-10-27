# data_processing.py
import pandas as pd
import json
from pymongo import MongoClient
import streamlit as st

# Conexión a MongoDB desde los Secrets de Streamlit
MONGODB_URI = st.secrets["MONGODB"]["URI"]
client = MongoClient(MONGODB_URI)
db = client['Llamadas123']  # Base de datos de llamadas

def get_data(opcion_analisis, year):
    # Seleccionar la colección correspondiente al año
    collection_name = f"llamadas{year}"
    collection = db[collection_name]

    # Pipeline para contar incidentes según la opción seleccionada
    if opcion_analisis == "Número de Incidentes":
        pipeline = [
            {
                "$group": {
                    "_id": "$LOCALIDAD",  # Agrupar por localidad
                    "INCIDENTES": {"$sum": {"$cond": [{"$ifNull": ["$FECHA_INICIO_DESPLAZAMIENTO_MOVIL", False]}, 1, 0]}}  # Contar cuando FECHA_INICIO_DESPLAZAMIENTO_MOVIL no sea nulo
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

    elif opcion_analisis == "Tipo de Incidente":
        pipeline = [
            {
                "$group": {
                    "_id": "$TIPO_INCIDENTE",  # Agrupar por tipo de incidente
                    "INCIDENTES": {"$sum": 1}  # Contar cada incidente
                }
            }
        ]
        df = pd.DataFrame(list(collection.aggregate(pipeline)))
        df.rename(columns={'_id': 'TIPO_INCIDENTE'}, inplace=True)
        color_var = "INCIDENTES"
        title = "Distribución de Incidentes por Tipo"

    # Cargar el archivo GeoJSON (puede estar predefinido en el proyecto)
    with open("localidades.geojson") as f:
        geojson = json.load(f)

    return df, geojson, color_var, title
