import streamlit as st
import plotly.express as px
import json

def load_geojson():
    with open('localidades.geojson', 'r') as f:
        return json.load(f)

def plot_call_count_map(data):
    st.title("Emergency Call Count in Bogotá by Locality")
    st.write("This map shows the number of emergency calls received in each locality in Bogotá.")
    
    geojson = load_geojson()
    fig = px.choropleth_mapbox(
        data,
        geojson=geojson,
        locations="LOCALIDAD",
        featureidkey="properties.Nombre de la localidad",
        color="count",
        color_continuous_scale="Viridis",
        mapbox_style="carto-positron",
        zoom=8.6,
        center={"lat": 4.2910, "lon": -74.1221},
    )
    st.plotly_chart(fig)

def plot_avg_age_map(data):
    st.title("Average Age in Bogotá by Locality")
    st.write("This map shows the average age of individuals involved in emergency calls across different localities.")

    geojson = load_geojson()
    fig = px.choropleth_mapbox(
        data,
        geojson=geojson,
        locations="LOCALIDAD",
        featureidkey="properties.Nombre de la localidad",
        color="avg_age",
        color_continuous_scale="RdBu",
        mapbox_style="carto-positron",
        zoom=8.6,
        center={"lat": 4.2910, "lon": -74.1221},
    )
    st.plotly_chart(fig)

def plot_age_distribution(data):
    st.title("Distribution of Ages in Emergency Calls")
    fig = px.histogram(data, x="EDAD", nbins=30, labels={"EDAD": "Age"})
    st.plotly_chart(fig)

def plot_incident_type_distribution(data):
    st.title("Incident Type Distribution")
    fig = px.treemap(data, path=["TIPO_INCIDENTE"], values="count", color="count", color_continuous_scale="Viridis")
    st.plotly_chart(fig)

def plot_gender_proportion(data):
    st.title("Proportion of Genders in Emergency Calls")
    fig = px.pie(data, names="GENERO", values="count")
    st.plotly_chart(fig)

def plot_incident_trend(data):
    st.title("Trend of Calls for 'Violencia Sexual' and 'Maltrato'")
    fig = px.line(data, x="year", y="count", color="incident_type", labels={"year": "Año", "count": "Llamadas"})
    st.plotly_chart(fig)
