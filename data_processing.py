import pandas as pd
import json
from pymongo import MongoClient
import streamlit as st
from datetime import datetime

# Conexión a MongoDB desde los Secrets de Streamlit
MONGODB_URI = st.secrets["MONGODB"]["URI"]
client = MongoClient(MONGODB_URI)
db = client['Llamadas123']  # Base de datos de llamadas

def get_data(opcion_analisis, year):
    # Determinar la colección a usar según el año
    collection_name = f'llamadas{year}'  # Cambiado para simplificar

    # Acceder a la colección correspondiente
    collection = db[collection_name]

    # Inicializar variables
    color_var = None
    title = ""
    df = pd.DataFrame()  # Inicializa df como un DataFrame vacío

    if opcion_analisis == "Número de Incidentes":
        pipeline = [
            {
                "$group": {
                    "_id": "$LOCALIDAD",  # Agrupar por localidad
                    "INCIDENTES": {"$sum": 1}  # Contar incidentes
                }
            }
        ]
        
        df = pd.DataFrame(list(collection.aggregate(pipeline)))
        df.rename(columns={'_id': 'LOCALIDAD'}, inplace=True)
        color_var = "INCIDENTES"
        title = "Número de Incidentes por Localidad"

    elif opcion_analisis == "Prioridad":
        pipeline = [
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
                    "_id": "$TIPO_INCIDENTE",
                    "INCIDENTES": {"$sum": 1}
                }
            }
        ]
        df = pd.DataFrame(list(collection.aggregate(pipeline)))
        df.rename(columns={'_id': 'TIPO_INCIDENTE'}, inplace=True)
        color_var = "INCIDENTES"
        title = "Distribución de Incidentes por Tipo"
        
    elif opcion_analisis == "Edad":
        # Obtener la edad promedio por localidad
        pipeline = [
            {
                "$match": {
                    "EDAD": {"$exists": True}  # Asegúrate de que la edad exista
                }
            },
            {
                "$group": {
                    "_id": "$LOCALIDAD",
                    "edad_promedio": {"$avg": "$EDAD"}  # Calcular la edad promedio
                }
            }
        ]
        df = pd.DataFrame(list(collection.aggregate(pipeline)))
        df.rename(columns={'_id': 'LOCALIDAD'}, inplace=True)
        if df.empty:
            df = pd.DataFrame(columns=["LOCALIDAD", "edad_promedio"])  # Asegurarnos de que el DataFrame tenga las columnas necesarias
        color_var = "edad_promedio"
        title = "Edad Promedio por Localidad"

    # Cargar el archivo GeoJSON (puede estar predefinido en el proyecto)
    with open("localidades.geojson") as f:
        geojson = json.load(f)

    return df, geojson, color_var, title
