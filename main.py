import pandas as pd
import json
import plotly.express as px
import streamlit as st
from datetime import datetime
from pymongo import MongoClient
import plotly.graph_objects as go

# Conectar a MongoDB
client = MongoClient("mongodb+srv://lsbdavidbernal:o8WZVSzPRkUr5NXo@llamadas123.ke4nc.mongodb.net/?retryWrites=true&w=majority&appName=Llamadas123")
db = client['Llamadas123']  # Base de datos de llamadas
collection = db['llamadas']  # Replace with your collection name

# Streamlit widgets to select date and time range with restricted year range
start_date = st.date_input(
    'Fecha Inicio', 
    datetime(2019, 1, 1),  # Default start date
    min_value=datetime(2019, 1, 1),  # Minimum date (2019)
    max_value=datetime(2023, 12, 31)  # Maximum date (2023)
)

end_date = st.date_input(
    'Fecha Fin', 
    datetime(2023, 12, 31),  # Default end date
    min_value=datetime(2019, 1, 1),  # Minimum date (2019)
    max_value=datetime(2023, 12, 31)  # Maximum date (2023)
)

start_hour = st.slider('Hora Inicio', 0, 23, 0)  # Default start hour
end_hour = st.slider('Hora Fin', 0, 23, 23)  # Default end hour

# Show the selected filters
st.write(f"Selected date range: {start_date} to {end_date}")
st.write(f"Selected hour range: {start_hour}:00 to {end_hour}:00")

# MongoDB query with filtering by date and hour for the call count map
pipeline_count = [
    {
        "$match": {
            "Año": {"$gte": start_date.year, "$lte": end_date.year},
            "Mes": {"$gte": start_date.month, "$lte": end_date.month},
            "Dia": {"$gte": start_date.day, "$lte": end_date.day},
            "Hora": {"$gte": start_hour, "$lte": end_hour}
        }
    },
    {
        "$group": {"_id": "$LOCALIDAD", "count": {"$sum": 1}}  # Group by LOCALIDAD and count calls
    }
]

# Execute the aggregation pipeline for call count
localidad_data_count = collection.aggregate(pipeline_count)

# Convert the data to a pandas DataFrame
df_localidad_count = pd.DataFrame(list(localidad_data_count))

# MongoDB query with filtering by date and hour for average age map
pipeline_avg_age = [
    {
        "$match": {
            "Año": {"$gte": start_date.year, "$lte": end_date.year},
            "Mes": {"$gte": start_date.month, "$lte": end_date.month},
            "Dia": {"$gte": start_date.day, "$lte": end_date.day},
            "Hora": {"$gte": start_hour, "$lte": end_hour}
        }
    },
    {
        "$group": {
            "_id": "$LOCALIDAD", 
            "avg_age": {"$avg": "$EDAD"}  # Calculate the average age (EDAD)
        }
    }
]

# Execute the aggregation pipeline for average age
localidad_data_avg_age = collection.aggregate(pipeline_avg_age)

# Convert the data to a pandas DataFrame
df_localidad_avg_age = pd.DataFrame(list(localidad_data_avg_age))

# MongoDB query for age distribution
pipeline_age = [
    {
        "$match": {
            "Año": {"$gte": start_date.year, "$lte": end_date.year},
            "Mes": {"$gte": start_date.month, "$lte": end_date.month},
            "Dia": {"$gte": start_date.day, "$lte": end_date.day},
            "Hora": {"$gte": start_hour, "$lte": end_hour}
        }
    },
    {
        "$project": {
            "EDAD": 1  # Only project the EDAD field
        }
    }
]

# Execute the aggregation pipeline for age distribution
localidad_data_age = collection.aggregate(pipeline_age)

# Convert the data to a pandas DataFrame
df_age = pd.DataFrame(list(localidad_data_age))

# MongoDB query for incident type distribution
pipeline_incident_type = [
    {
        "$match": {
            "Año": {"$gte": start_date.year, "$lte": end_date.year},
            "Mes": {"$gte": start_date.month, "$lte": end_date.month},
            "Dia": {"$gte": start_date.day, "$lte": end_date.day},
            "Hora": {"$gte": start_hour, "$lte": end_hour}
        }
    },
    {
        "$group": {
            "_id": "$TIPO_INCIDENTE",  # Group by the TIPO_INCIDENTE field
            "count": {"$sum": 1}  # Count the number of incidents for each type
        }
    }
]

# Execute the aggregation pipeline for incident type counts
incident_data = collection.aggregate(pipeline_incident_type)

# Convert the data to a pandas DataFrame
df_incident_type = pd.DataFrame(list(incident_data))

# MongoDB query for gender distribution
pipeline_gender = [
    {
        "$match": {
            "Año": {"$gte": start_date.year, "$lte": end_date.year},
            "Mes": {"$gte": start_date.month, "$lte": end_date.month},
            "Dia": {"$gte": start_date.day, "$lte": end_date.day},
            "Hora": {"$gte": start_hour, "$lte": end_hour}
        }
    },
    {
        "$group": {
            "_id": "$GENERO",  # Group by gender
            "count": {"$sum": 1}  # Count the occurrences of each gender
        }
    }
]

# Execute the aggregation pipeline for gender distribution
localidad_data_gender = collection.aggregate(pipeline_gender)

# Convert the data to a pandas DataFrame
df_gender = pd.DataFrame(list(localidad_data_gender))

# MongoDB query for comparing "Violencia Sexual" and "Maltrato" over years with hour filter
pipeline_incident_trend = [
    {
        "$match": {
            "TIPO_INCIDENTE": {"$in": ["Violencia Sexual", "Maltrato"]},
            "Año": {"$gte": 2019, "$lte": 2023},
            "Mes": {"$gte": start_date.month, "$lte": end_date.month},
            "Dia": {"$gte": start_date.day, "$lte": end_date.day},
            "Hora": {"$gte": start_hour, "$lte": end_hour}
        }
    },
    {
        "$group": {
            "_id": {"year": "$Año", "incident_type": "$TIPO_INCIDENTE"},
            "count": {"$sum": 1}
        }
    },
    {
        "$sort": {"_id.year": 1}  # Sort by year for chronological order
    }
]

# MongoDB query to get gender distribution per year for "Violencia Sexual" and "Maltrato"
pipeline_gender_trend = [
    {
        "$match": {
            "TIPO_INCIDENTE": {"$in": ["Violencia Sexual", "Maltrato"]},
            "Año": {"$gte": 2019, "$lte": 2023},
            "Mes": {"$gte": start_date.month, "$lte": end_date.month},
            "Dia": {"$gte": start_date.day, "$lte": end_date.day},
            "Hora": {"$gte": start_hour, "$lte": end_hour}
        }
    },
    {
        "$group": {
            "_id": {"year": "$Año", "incident_type": "$TIPO_INCIDENTE", "gender": "$GENERO"},
            "count": {"$sum": 1}
        }
    },
    {
        "$sort": {"_id.year": 1}  # Sort by year for chronological order
    }
]

# Execute the aggregation pipeline for gender trend data
gender_trend_data = collection.aggregate(pipeline_gender_trend)
df_gender_trend = pd.DataFrame(list(gender_trend_data))

# Execute the aggregation pipeline for incident trend data
incident_trend_data = collection.aggregate(pipeline_incident_trend)
df_incident_trend = pd.DataFrame(list(incident_trend_data))

# MongoDB pipeline for choropleth map data on "Violencia Sexual" and "Maltrato" by locality
pipeline_choropleth = [
    {
        "$match": {
            "TIPO_INCIDENTE": {"$in": ["Violencia Sexual", "Maltrato"]},
            "Año": {"$gte": start_date.year, "$lte": end_date.year},
            "Mes": {"$gte": start_date.month, "$lte": end_date.month},
            "Dia": {"$gte": start_date.day, "$lte": end_date.day},
            "Hora": {"$gte": start_hour, "$lte": end_hour}
        }
    },
    {
        "$group": {
            "_id": "$LOCALIDAD",
            "call_count": {"$sum": 1}  # Count incidents per locality
        }
    }
]

# Execute aggregation pipeline for choropleth data
choropleth_data = collection.aggregate(pipeline_choropleth)

# Convert the data to a pandas DataFrame and rename columns
df_choropleth = pd.DataFrame(list(choropleth_data))

# Check if the DataFrames are empty
if df_localidad_avg_age.empty or df_localidad_count.empty or df_age.empty or df_incident_type.empty or df_gender.empty or df_incident_trend.empty or df_choropleth.empty or df_gender_trend.empty:
    st.write("No data available for the selected date and time range.")
else:
    # Ensure the columns are properly renamed for consistency
    df_localidad_count = df_localidad_count.rename(columns={"_id": "LOCALIDAD"})
    df_localidad_avg_age = df_localidad_avg_age.rename(columns={"_id": "LOCALIDAD"})
    df_incident_type = df_incident_type.rename(columns={"_id": "TIPO_INCIDENTE"})
    df_gender = df_gender.rename(columns={"_id": "GENERO"})
    df_incident_trend["year"] = df_incident_trend["_id"].apply(lambda x: x["year"])
    df_incident_trend["incident_type"] = df_incident_trend["_id"].apply(lambda x: x["incident_type"])
    df_incident_trend = df_incident_trend.drop(columns="_id")  # Drop the original '_id' column
    df_choropleth = df_choropleth.rename(columns={"_id": "LOCALIDAD", "call_count": "Total Calls"})
    df_gender_trend["year"] = df_gender_trend["_id"].apply(lambda x: x["year"])
    df_gender_trend["incident_type"] = df_gender_trend["_id"].apply(lambda x: x["incident_type"])
    df_gender_trend["gender"] = df_gender_trend["_id"].apply(lambda x: x["gender"])
    df_gender_trend = df_gender_trend.drop(columns="_id")  # Drop the original '_id' column

    # Load the GeoJSON file for localities
    with open('localidades.geojson', 'r') as f:  # Replace with your GeoJSON file path
        geojson = json.load(f)
    
    # Apply bounding box to the call count map
    fig_call_count = px.choropleth_mapbox(
        df_localidad_count,
        geojson=geojson,
        locations="LOCALIDAD",
        featureidkey="properties.Nombre de la localidad",
        color="count",
        color_continuous_scale="Viridis",
        center={"lat": 4.2910, "lon": -74.1221},  # Center of bounding box
        mapbox_style="carto-positron",
        zoom=8.6,
        title="Emergency Call Count in Bogotá by Locality",
        hover_data={"count": ":,.0f"},
    )

    st.plotly_chart(fig_call_count)

    # Create the choropleth map for average age
    fig_avg_age = px.choropleth_mapbox(
        df_localidad_avg_age,  # The DataFrame containing the average age per LOCALIDAD
        geojson=geojson,  # The GeoJSON data for the localities
        locations="LOCALIDAD",  # Field in df_localidad_avg_age for matching
        featureidkey="properties.Nombre de la localidad",  # Field in the GeoJSON for matching
        color="avg_age",  # Column in df_localidad_avg_age for coloring the map (average age)
        color_continuous_scale="Blues",  # A different color scale for the map (RdBu)
        center={"lat": 4.2910, "lon": -74.1221},  # Center of the map (Bogotá)
        mapbox_style="carto-positron",  # Style of the map
        zoom=8.6,  # Zoom level
        title="Average Age in Bogotá by Locality",  # Map title
        hover_data={"avg_age": ":,.0f"}  # Formatting the hover data (showing numbers with commas)
    )

    # Display the choropleth map for average age
    st.plotly_chart(fig_avg_age)

    # Create the histogram for age distribution
    fig_age_dist = px.histogram(
        df_age,  # DataFrame containing the EDAD field
        x="EDAD",  # Use the EDAD field for the x-axis
        nbins=30,  # Number of bins for the histogram
        title="Distribution of Ages in Emergency Calls",  # Histogram title
        labels={"EDAD": "Age"},  # Axis label
        color_discrete_sequence=["#636EFA"],  # Color for the bars
    )

    # Display the histogram for age distribution
    st.plotly_chart(fig_age_dist)

    # Create the treemap for incident types
    fig_incident_type = px.treemap(
        df_incident_type,  # The DataFrame containing incident type counts
        path=["TIPO_INCIDENTE"],  # Field for grouping data in the treemap
        values="count",  # Values to size the rectangles (incident count)
        title="Incident Type Distribution",  # Title of the treemap
        color="count",  # Color the rectangles by the incident count
        color_continuous_scale="Viridis",  # Color scale for the rectangles
        hover_data=["TIPO_INCIDENTE", "count"],  # Display type and count on hover
    )

    # Display the treemap for incident types
    st.plotly_chart(fig_incident_type)

    # Create the pie chart for gender distribution
    fig_gender_pie = px.pie(
        df_gender,  # DataFrame containing the gender data
        names="GENERO",  # Gender column for slices
        values="count",  # Count column for slice sizes
        title="Proportion of Genders in Emergency Calls",  # Pie chart title
        color="GENERO",  # Color by gender
        color_discrete_sequence=["#636EFA", "#F7B801", "#FF4F64"]  # Custom color palette
    )

    # Display the pie chart for gender distribution
    st.plotly_chart(fig_gender_pie)

    # Create the combined line and bar chart
    fig_trend_combined = go.Figure()

    # Add line traces for each incident type
    for incident in df_incident_trend['incident_type'].unique():
        incident_data = df_incident_trend[df_incident_trend["incident_type"] == incident]
        fig_trend_combined.add_trace(
            go.Scatter(
                x=incident_data["year"],
                y=incident_data["count"],
                mode="lines+markers",
                name=incident,
                line_shape="linear"
            )
        )

    # Add bar traces for each gender proportion by year
    for gender in df_gender_trend["gender"].unique():
        gender_data = df_gender_trend[df_gender_trend["gender"] == gender]
        fig_trend_combined.add_trace(
            go.Bar(
                x=gender_data["year"],
                y=gender_data["count"],
                name=f"Gender: {gender}",
                opacity=0.6,
                yaxis="y2"
            )
        )

    # Update layout to include a secondary y-axis for the bar chart
    fig_trend_combined.update_layout(
        title="Trend of Calls for 'Violencia Sexual' and 'Maltrato' with Gender Proportion",
        xaxis_title="Año",
        yaxis=dict(title="Llamadas (Line Chart)"),
        yaxis2=dict(
            title="Proportion by Gender (Bar Chart)",
            overlaying="y",
            side="right"
        ),
        barmode="stack",
    )

    # Display the combined chart
    st.plotly_chart(fig_trend_combined)

    # Create the choropleth map for incident counts in localities
    fig_choropleth = px.choropleth_mapbox(
        df_choropleth,
        geojson=geojson,
        locations="LOCALIDAD",
        featureidkey="properties.Nombre de la localidad",
        color="Total Calls",
        color_continuous_scale="Oranges",
        center={"lat": 4.2910, "lon": -74.1221},
        mapbox_style="carto-positron",
        zoom=8.6,
        title="Number of 'Violencia Sexual' and 'Maltrato' Calls in Bogotá by Locality",
        hover_data={"Total Calls": ":,.0f"},
    )

    # Display the choropleth map
    st.plotly_chart(fig_choropleth)
