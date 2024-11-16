import pandas as pd
import json
from pymongo import MongoClient
import streamlit as st
from datetime import datetime

# Conexión a MongoDB desde los Secrets de Streamlit
MONGODB_URI = st.secrets["MONGODB"]["URI"]
client = MongoClient(MONGODB_URI)
db = client['123']  # Base de datos de llamadas

def get_aggregated_data_by_incident_and_gender(years, db): 
    data_frames = []

    for year in years:
        # Nombre de la colección
        collection_name = f"llamadas{year}"
        collection = db[collection_name]

        # Pipeline para filtrar y agrupar
        pipeline = [
            {
                "$match": {
                    "TIPO_INCIDENTE": {"$in": ["Violencia Sexual", "Maltrato"]},
                    "GENERO": {"$exists": True, "$ne": "N/A"}  # Excluir valores nulos o "N/A"
                }
            },
            {
                "$group": {
                    "_id": {"TIPO_INCIDENTE": "$TIPO_INCIDENTE", "GENERO": "$GENERO"},
                    "count": {"$sum": 1}
                }
            }
        ]

        # Ejecutar el pipeline
        results = list(collection.aggregate(pipeline))

        # Convertir resultados a DataFrame
        df = pd.DataFrame(results)

        if not df.empty:
            # Expandir los campos del _id
            df['TIPO_INCIDENTE'] = df['_id'].apply(lambda x: x.get('TIPO_INCIDENTE'))
            df['GENERO'] = df['_id'].apply(lambda x: x.get('GENERO'))
            df['YEAR'] = year  # Añadir el año como columna
            df.drop(columns=['_id'], inplace=True)

            data_frames.append(df)

    # Concatenar todos los DataFrames
    if data_frames:
        combined_df = pd.concat(data_frames, ignore_index=True)
    else:
        combined_df = pd.DataFrame(columns=["TIPO_INCIDENTE", "GENERO", "count", "YEAR"])

    return combined_df

def get_data(opcion_analisis, year, geojson_file="localidades.geojson"):
    try:
        # Determinar la colección a usar según el año
        collection_name = f'llamadas{year}'
        collection = db[collection_name]
    except Exception as e:
        raise ValueError(f"Error al acceder a la colección: {e}")

    # Inicializar variables
    color_var = None
    title = ""
    df = pd.DataFrame()

    try:
        if opcion_analisis == "Número de Incidentes":
            pipeline = [
                {"$group": {"_id": "$LOCALIDAD", "INCIDENTES": {"$sum": 1}}}
            ]
            df = pd.DataFrame(list(collection.aggregate(pipeline)))
            df.rename(columns={'_id': 'LOCALIDAD'}, inplace=True)
            color_var = "INCIDENTES"
            title = "Número de Incidentes por Localidad"

        elif opcion_analisis == "Prioridad":
            pipeline = [
                {"$group": {"_id": {"LOCALIDAD": "$LOCALIDAD", "PRIORIDAD": "$PRIORIDAD"}, 
                            "INCIDENTES": {"$sum": 1}}},
                {"$sort": {"_id.LOCALIDAD": 1, "INCIDENTES": -1}}
            ]
            df = pd.DataFrame(list(collection.aggregate(pipeline)))
            if not df.empty:
                df['LOCALIDAD'] = df['_id'].apply(lambda x: x.get('LOCALIDAD'))
                df['PRIORIDAD'] = df['_id'].apply(lambda x: x.get('PRIORIDAD'))
                df.drop(columns=['_id'], inplace=True)

        elif opcion_analisis == "Tipo de Incidente":
            pipeline = [{"$group": {"_id": "$TIPO_INCIDENTE", "INCIDENTES": {"$sum": 1}}}]
            df = pd.DataFrame(list(collection.aggregate(pipeline)))
            df.rename(columns={'_id': 'TIPO_INCIDENTE'}, inplace=True)
            color_var = "INCIDENTES"
            title = "Distribución de Incidentes por Tipo"

        elif opcion_analisis == "Edad por Localidad":
            pipeline = [
                {"$match": {"EDAD": {"$exists": True, "$ne": None}}},
                {"$group": {"_id": "$LOCALIDAD", "avg_age": {"$avg": "$EDAD"}}}
            ]
            df = pd.DataFrame(list(collection.aggregate(pipeline)))
            df.rename(columns={'_id': 'LOCALIDAD'}, inplace=True)
            color_var = "avg_age"
            title = "Distribución de Edad por Localidad"

        elif opcion_analisis == "Violencia sexual y maltrato por localidad":
            pipeline = [
                {
                    "$match":{
                    "TIPO_INCIDENTE":{"$in":["Violencia Sexual","Maltrato"]}
                    }
                },
                {
                    "$group": {
                        "_id": "$LOCALIDAD",  # Agrupar por localidad
                        "call_count": {"$sum": 1}  # Contar incidentes por localidad
                    }
                }
            ]
            df = pd.DataFrame(list(collection.aggregate(pipeline)))
            df.rename(columns={'_id': 'LOCALIDAD'}, inplace=True)
            color_var = "call_count"
            title = "Distribución de Violencia Sexual y Maltrato por Localidad"

    except Exception as e:
        raise ValueError(f"Error al ejecutar pipeline: {e}")

    # Cargar GeoJSON
    try:
        with open(geojson_file) as f:
            geojson = json.load(f)
    except Exception as e:
        raise FileNotFoundError(f"Error al cargar el archivo GeoJSON: {e}")

    return df, geojson, color_var, title
