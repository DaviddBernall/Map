import pandas as pd
from datetime import datetime
from pymongo import MongoClient

# Conexión a MongoDB desde los Secrets de Streamlit
MONGODB_URI = st.secrets["MONGODB"]["URI"]
client = MongoClient(MONGODB_URI)
db = client['Llamadas123']  # Base de datos de llamadas
collection = db['llamadas']  # Replace with your collection name

def get_filtered_data(start_date, end_date, start_hour, end_hour):
    # Common filter for date and hour range
    filter_pipeline = [
        {
            "$match": {
                "Año": {"$gte": start_date.year, "$lte": end_date.year},
                "Mes": {"$gte": start_date.month, "$lte": end_date.month},
                "Dia": {"$gte": start_date.day, "$lte": end_date.day},
                "Hora": {"$gte": start_hour, "$lte": end_hour}
            }
        }
    ]
    return filter_pipeline

def get_call_count_data(start_date, end_date, start_hour, end_hour):
    pipeline = get_filtered_data(start_date, end_date, start_hour, end_hour) + [
        {"$group": {"_id": "$LOCALIDAD", "count": {"$sum": 1}}}
    ]
    return pd.DataFrame(list(collection.aggregate(pipeline))).rename(columns={"_id": "LOCALIDAD"})

def get_avg_age_data(start_date, end_date, start_hour, end_hour):
    pipeline = get_filtered_data(start_date, end_date, start_hour, end_hour) + [
        {"$group": {"_id": "$LOCALIDAD", "avg_age": {"$avg": "$EDAD"}}}
    ]
    return pd.DataFrame(list(collection.aggregate(pipeline))).rename(columns={"_id": "LOCALIDAD"})

def get_age_distribution(start_date, end_date, start_hour, end_hour):
    pipeline = get_filtered_data(start_date, end_date, start_hour, end_hour) + [
        {"$project": {"EDAD": 1}}
    ]
    return pd.DataFrame(list(collection.aggregate(pipeline)))

def get_incident_type_data(start_date, end_date, start_hour, end_hour):
    pipeline = get_filtered_data(start_date, end_date, start_hour, end_hour) + [
        {"$group": {"_id": "$TIPO_INCIDENTE", "count": {"$sum": 1}}}
    ]
    return pd.DataFrame(list(collection.aggregate(pipeline))).rename(columns={"_id": "TIPO_INCIDENTE"})

def get_gender_distribution(start_date, end_date, start_hour, end_hour):
    pipeline = get_filtered_data(start_date, end_date, start_hour, end_hour) + [
        {"$group": {"_id": "$GENERO", "count": {"$sum": 1}}}
    ]
    return pd.DataFrame(list(collection.aggregate(pipeline))).rename(columns={"_id": "GENERO"})

def get_incident_trend_data(start_date, end_date, start_hour, end_hour):
    pipeline = get_filtered_data(start_date, end_date, start_hour, end_hour) + [
        {
            "$match": {
                "TIPO_INCIDENTE": {"$in": ["Violencia Sexual", "Maltrato"]}
            }
        },
        {"$group": {"_id": {"year": "$Año", "incident_type": "$TIPO_INCIDENTE"}, "count": {"$sum": 1}}},
        {"$sort": {"_id.year": 1}}
    ]
    data = pd.DataFrame(list(collection.aggregate(pipeline)))
    data["year"] = data["_id"].apply(lambda x: x["year"])
    data["incident_type"] = data["_id"].apply(lambda x: x["incident_type"])
    return data.drop(columns=["_id"])
