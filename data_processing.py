import pandas as pd
import json
from pymongo import MongoClient
import streamlit as st

# Conexión a MongoDB desde los Secrets de Streamlit
MONGODB_URI = st.secrets["MONGODB"]["URI"]
client = MongoClient(MONGODB_URI)
db = client['Llamadas123']  # Base de datos de llamadas

def get_data(opcion_analisis, año, start_datetime, end_datetime):
    # Debugging: Verificar los valores de año, fechas y horas
    st.write(f"Año seleccionado: {año}")
    st.write(f"Fecha de inicio: {start_datetime}")
    st.write(f"Fecha de fin: {end_datetime}")
    
    try:
        # Seleccionar la colección según el año
        collection = db[f'llamadas{año}']
        st.write(f"Conectado a la colección: llamadas{año}")
    except Exception as e:
        st.error(f"Error conectando a la colección: {e}")
        return pd.DataFrame(), None, None, None

    # Pipeline básico para contar incidentes filtrados por fecha y hora
    match_stage = {
        "$match": {
            "FECHA_INICIO_DESPLAZAMIENTO_MOVIL": {
                "$gte": start_datetime,
                "$lte": end_datetime
            }
        }
    }

    try:
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
            st.write("Datos cargados correctamente para Número de Incidentes")
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
            st.write("Datos cargados correctamente para Prioridad")
            df['LOCALIDAD'] = df['_id'].apply(lambda x: x['LOCALIDAD'])
            df['PRIORIDAD'] = df['_id'].apply(lambda x: x['PRIORIDAD'])
            df.drop(columns=['_id'], inplace=True)
            color_var = None
            title = "Incidentes por Prioridad y Localidad"
    except Exception as e:
        st.error(f"Error al ejecutar la consulta: {e}")
        return pd.DataFrame(), None, None, None

    # Cargar el archivo GeoJSON
    try:
        with open("localidades.geojson") as f:
            geojson = json.load(f)
    except Exception as e:
        st.error(f"Error al cargar el archivo GeoJSON: {e}")
        return pd.DataFrame(), None, None, None

    return df, geojson, color_var, title
