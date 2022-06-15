

# If you prefer to run the code online instead of on your computer click:
# https://github.com/Coding-with-Adam/Dash-by-Plotly#execute-code-in-browser

from curses import color_content
import imp
from dash import Dash, dcc, Output, Input, html  # pip install dash
# pip install dash-bootstrap-components
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd                        # pip install pandas
import plotly.graph_objects as go
import json
import geopandas as gpd

# incorporate data into app
# Source - https://www.cdc.gov/nchs/pressroom/stats_of_the_states.htm
df2 = pd.read_csv("finalValuesTemperature.csv")
df = pd.read_csv("newNiveauMer.csv")
counties = gpd.read_file("custom.geo.json")

# Build your components
app = Dash(__name__)
mytitle = dcc.Markdown(children='')






fig = px.choropleth_mapbox(df, geojson=counties, locations='pays', featureidkey="properties.iso_a3", color='total',
                           color_continuous_scale="Viridis",mapbox_style="carto-positron",
                           
                           )

""""

fig = px.choropleth(data_frame=df, geojson=counties,
                        locations = df.index,
                        scope="world",
                        height=600,
                        color= "values",
                        )
                        
"""


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
