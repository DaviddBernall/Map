import plotly.express as px
import streamlit as st

# Función para crear el mapa coroplético
def create_map(df, geojson, color_var, title,color):
    fig = px.choropleth_mapbox(
        df, 
        geojson=geojson, 
        locations="LOCALIDAD", 
        featureidkey="properties.Nombre de la localidad", 
        color=color_var,  
        color_continuous_scale=color, 
        center={"lat": 4.2910, "lon": -74.1221}, 
        mapbox_style="carto-positron", 
        zoom=8.6, 
        title=title,
        hover_data={color_var: ':,.0f'}  # Formato para mostrar el número completo con separador de miles
    )
    
    # Configuración de la leyenda para mostrar números completos con separador de miles
    fig.update_layout(coloraxis_colorbar=dict(tickformat=',.0f'))  # Separador de miles en la leyenda
    
    return fig

# Función para crear el gráfico de barras
def create_bar_chart(df, title):
    # Formatear las cantidades para agregar separador de miles
    df['INCIDENTES'] = df['INCIDENTES'].map(lambda x: f"{x:,.0f}")  # Formato con separador de miles
    
    fig = px.bar(
        df, 
        x='LOCALIDAD', 
        y='INCIDENTES', 
        color='PRIORIDAD', 
        title=title, 
        labels={'INCIDENTES': 'Número de Incidentes', 'LOCALIDAD': 'Localidad'},
        color_discrete_sequence=px.colors.qualitative.Vivid,
        text='INCIDENTES'  # Usar la columna formateada como texto
    )
    
    # Formatear el eje Y para mostrar separador de miles
    fig.update_layout(yaxis_tickformat=',')  # Separador de miles en el eje Y

    return fig

# Función para crear el treemap
def create_treemap(df, title):
    fig = px.treemap(df, 
                     path=['TIPO_INCIDENTE'], 
                     values='INCIDENTES', 
                     title=title,
                     color='INCIDENTES',
                     color_continuous_scale='Viridis',
                     labels={'TIPO_INCIDENTE': 'Tipo de Incidente', 'INCIDENTES': 'Número de Incidentes'})
    return fig

def create_histogram(df, title):
    fig = px.histogram(
        df, 
        x='EDAD', 
        title=title, 
        nbins=20)

    # Agregar borde a cada barra
    fig.update_traces(marker=dict(line=dict(color='black', width=1)))  # Color y ancho del borde

    # Actualiza el formato del eje x
    fig.update_layout(
        xaxis_title='Edad',
        yaxis_title='Número de Incidentes',
        title=title
    )

    return fig

def create_segmented_bar_chart(df, title):
    if df.empty:
        raise ValueError("El DataFrame está vacío. No se puede crear el gráfico.")

    # Crear gráfico con Plotly Express
    fig = px.bar(
        df,
        x="YEAR",
        y="count",
        color="GENERO",
        facet_col="TIPO_INCIDENTE",
        title=title,
        labels={"count": "Cantidad de Incidentes", "YEAR": "Año", "GENERO": "Género"},
        barmode="stack",  # Barras segmentadas
        text="count"      # Mostrar los valores
    )

    # Actualizar diseño
    fig.update_traces(textposition='inside')
    fig.update_layout(
        legend_title="Género",
        xaxis=dict(title="Año"),
        yaxis=dict(title="Cantidad de Incidentes"),
        margin=dict(t=50, b=50, l=50, r=50),
        height=600,
    )

    return fig
