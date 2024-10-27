import plotly.express as px

# Función para crear el mapa coroplético
def create_map(df, geojson, color_var, title):
    fig = px.choropleth_mapbox(df, 
                               geojson=geojson, 
                               locations="LOCALIDAD", 
                               featureidkey="properties.Nombre de la localidad", 
                               color=color_var,  
                               color_continuous_scale="Viridis", 
                               center={"lat": 4.2910, "lon": -74.1221}, 
                               mapbox_style="carto-positron", 
                               zoom=8.6, 
                               width=None,  # Ajustar automáticamente
                               height=None,  # Ajustar automáticamente
                               title=title)
    return fig

# Función para crear el gráfico de barras
def create_bar_chart(df, title):
    fig = px.bar(df, 
                 x='LOCALIDAD', 
                 y='INCIDENTES', 
                 color='PRIORIDAD', 
                 title=title, 
                 labels={'INCIDENTES': 'Número de Incidentes', 'LOCALIDAD': 'Localidad'},
                 color_discrete_sequence=px.colors.qualitative.Vivid)
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
