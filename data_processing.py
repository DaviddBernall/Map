import pandas as pd
import json
from pymongo import MongoClient
import streamlit as st
from datetime import datetime

# Conexión a MongoDB desde los Secrets de Streamlit
client = MongoClient("mongodb://localhost:27017/")
db = client["llamadas123"]

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
                    "_id": {"LOCALIDAD": "$LOCALIDAD", "PRIORIDAD": "$PRIORIDAD"},
                    "INCIDENTES": {"$sum": 1}
                }
            },
            {
                "$sort": {"_id.LOCALIDAD": 1, "INCIDENTES": -1}
            }
        ]
        df = pd.DataFrame(list(collection.aggregate(pipeline)))
        df['LOCALIDAD'] = df['_id'].apply(lambda x: x.get('LOCALIDAD') if isinstance(x, dict) else None)
        df['PRIORIDAD'] = df['_id'].apply(lambda x: x.get('PRIORIDAD') if isinstance(x, dict) else None)
        df.drop(columns=['_id'], inplace=True)

    elif opcion_analisis == "Tipo de Incidente":  # Asegúrate de agregar esta condición
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
        pipeline = [
            {
                "$match": {
                    "EDAD": {"$exists": True, "$gt": 0}  # Excluir edades no válidas
                }
            },
            {
                "$group": {
                    "_id": "$LOCALIDAD",
                    "EDAD_PROMEDIO": {"$avg": "$EDAD"}  # Calcular promedio de edad
                }
            }
        ]
        
        df = pd.DataFrame(list(collection.aggregate(pipeline)))
        if df.empty:
            df = pd.DataFrame(columns=["EDAD"])  # Asegurarnos de que el DataFrame tenga la columna EDAD
        color_var = None
        title = "Distribución de Edades"

    # Cargar el archivo GeoJSON (puede estar predefinido en el proyecto)
    with open("localidades.geojson") as f:
        geojson = json.load(f)

    return df, geojson, color_var, title
