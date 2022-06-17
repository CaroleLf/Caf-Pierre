from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd                     
import plotly.graph_objects as go
import geopandas as gpd

df = pd.read_csv("newNiveauMer.csv")
df2 = pd.read_csv("finalValuesTemperature.csv")

counties = gpd.read_file("custom.geo.json")

app = Dash(__name__)
mytitle = dcc.Markdown(children='')



fig = px.choropleth_mapbox(df, geojson=counties, locations='pays', featureidkey="properties.iso_a3", color='total',
                           color_continuous_scale="Viridis",mapbox_style="carto-positron",
                           
                           )


fig2 = go.Figure(data=go.Scattergeo(
    lon=df2['longitude'],
    lat=df2['latitude'],
    mode='markers',
    marker_color=df2['values'],

))

df3 = pd.read_csv("average.csv")

fig3 = px.bar(df3, x='country', y='values', color='values', barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Identified Geothermal Systems of the Western USA'),
    html.Div(children='''
        This data was provided by the USGS.
    '''),
    dcc.Graph(
        id='Temperature',
        figure=fig
    ),
   
    html.H2(children='Map of the montée des océans'),
    html.Div(children='''
        This data was provided by me.
    '''),
    
    dcc.Graph(
        id='Map ocean',
        figure=fig2
    ),
    
    html.H2(children='Average temperature evolution diagram from 2041 - 2060 based on 1995 - 2014 '),
    html.Div(children='''
        This data was provided by ipcc.
    '''),

    dcc.Graph(
        id='Average Temperature',
        figure=fig3
    )
])


# Run app

if __name__ == '__main__':
    app.run_server(debug=True)
