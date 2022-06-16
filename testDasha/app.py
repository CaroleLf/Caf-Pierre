from gc import callbacks
from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
import geopandas as gpd

#############################################################################################################################

dfPibPays = pd.read_csv("/home/etd/projet/SAE2.04_2.05_equipe4/script-df/pib.csv", usecols=['Country Name', '2020'])
dfPopulationPays = pd.read_csv("/home/etd/projet/SAE2.04_2.05_equipe4/script-df/pop_totale.csv", usecols=['Country Name', '2020'])
dfEmpreinteCarbone = pd.read_csv("/home/etd/projet/SAE2.04_2.05_equipe4/testDasha/empreinte_carbone.csv", usecols=['Country Name', '2014'])
dfEmpreinteCarone30years = pd.read_csv("/home/etd/projet/SAE2.04_2.05_equipe4/testDasha/empreinte_carbone.csv", usecols=['Country Name', "1984","1985","1986","1987","1988","1989","1990","1991","1992","1993","1994","1995","1996","1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014"])
dfSeaLevel = pd.read_csv("/home/etd/projet/SAE2.04_2.05_equipe4/testDasha/NiveauMerUpdate.csv")
dfTemperatureForecast = pd.read_csv("/home/etd/projet/SAE2.04_2.05_equipe4/testDasha/AllTemperatureMean2041-2060Pays.csv")
dfAverageTemperature = pd.read_csv("/home/etd/projet/SAE2.04_2.05_equipe4/testDasha/AverageTemperature1941-1960.csv")
counties = gpd.read_file("/home/etd/projet/SAE2.04_2.05_equipe4/custom.geo.json")

#############################################################################################################################

dateVoulue = ["1986-01-01 00:00:00",
"1987-01-01 00:00:00",
"1988-01-01 00:00:00",
"1989-01-01 00:00:00",
"1990-01-01 00:00:00",
"1991-01-01 00:00:00",
"1992-01-01 00:00:00",
"1993-01-01 00:00:00",
"1994-01-01 00:00:00",
"1995-01-01 00:00:00",
"1996-01-01 00:00:00",
"1997-01-01 00:00:00",
"1998-01-01 00:00:00",
"1999-01-01 00:00:00",
"2000-01-01 00:00:00",
"2001-01-01 00:00:00",
"2002-01-01 00:00:00",
"2003-01-01 00:00:00",
"2004-01-01 00:00:00",
"2005-01-01 00:00:00",
"2006-01-01 00:00:00",
"2007-01-01 00:00:00",
"2008-01-01 00:00:00",
"2009-01-01 00:00:00",
"2010-01-01 00:00:00",
"2011-01-01 00:00:00",
"2012-01-01 00:00:00",
"2013-01-01 00:00:00",
"2014-01-01 00:00:00",
"2015-01-01 00:00:00",
"2016-01-01 00:00:00"
]

def setDateVoulue(df):
    return df[df["Unnamed: 0"].isin(dateVoulue)]

penergyfrance = pd.read_csv("testDasha/primary_energy/primary_energy_france.csv", sep=';')
penergyfrance = setDateVoulue(penergyfrance)

penergychina = pd.read_csv("testDasha/primary_energy/primary_energy_china.csv", sep=';')
penergychina = setDateVoulue(penergychina)

penergycoteivoire = pd.read_csv("testDasha/primary_energy/primary_energy_coteivoire.csv", sep=';')
penergycoteivoire = setDateVoulue(penergycoteivoire)

penergyindia = pd.read_csv("testDasha/primary_energy/primary_energy_india.csv", sep=';')
penergyindia = setDateVoulue(penergyindia)

penergydenmark = pd.read_csv("testDasha/primary_energy/primary_energy_denmark.csv", sep=';')
penergydenmark = setDateVoulue(penergydenmark)

penergyunitedstates = pd.read_csv("testDasha/primary_energy/primary_energy_unitedstates.csv", sep=';')
penergyunitedstates = setDateVoulue(penergyunitedstates)

#############################################################################################################################


app = Dash(__name__, suppress_callback_exceptions=True)



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])



#############
# page home #
#############
index_page = html.Div([
    html.H1('CoffeePierre'),
    #html.Img(src='logo.png'),
    dcc.Link('Go to Country', href='/country'),
    html.Br(),
    html.Br(),
    dcc.Link('Go to Map', href='/map'),
], style = {'text-align': 'center'})

################
# page country #
################
country_layout = html.Div([
    html.H1('Country'),
    html.Br(),
    dcc.Link('Display the primary energy consumption of a country', href='/primary-energy'),
    html.Br(),
    html.Br(),
    dcc.Link('Display the GDP, population and GDP per capita of a country', href='/gdp-pop'),
    html.Br(),
    html.Br(),
    dcc.Link('Display the carbon footprint of a country', href='/carbon-footprint'),
    html.Br(),
    html.Br(),
    dcc.Link("Display the evolution of a country's carbon footprint over 30 years", href='/carbon-footprint-30'),
    html.Br(),
    html.Br(),
    dcc.Link("Display a country's carbon footprint compared to the global footprint", href='/carbon-footprint-global'),
    html.Br(),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
], style = {'text-align': 'center'})

#######################
# page primary-energy #
#######################



primary_energy_layout = html.Div([
    dcc.Link('Go back to Country', href='/country'),
    html.Br(),
    html.H1('Choice a country for see the primary energy consumption'),
    html.Br(),
    dcc.Dropdown(["France", "Denmark", "Cote d'Ivoire", "China", "India", "United States"], id='country-dropdown'),
    html.Br(),
    html.Div(id='country-choice'),
    html.Br(),
    html.Div(id="report-primary-energy"),
], style = {'text-align': 'center'})
@callback(Output('country-choice', 'children'), Input('country-dropdown', 'value'))
def retGraphPrimaryEnergy(value):
    if value == "France":
        df = penergyfrance
    if value == "Denmark":
        df = penergydenmark
    if value == "Cote d'Ivoire":
        df = penergycoteivoire
    if value == "China":
        df = penergychina
    if value == "India":
        df = penergyindia
    if value == "United States":
        df = penergyunitedstates
    return dcc.Graph(
        figure = {
            'data': [
                {'x': df['Unnamed: 0'], 'y': df['Oil'], 'type': 'line', 'name': 'Oil'},
                {'x': df['Unnamed: 0'], 'y': df['Coal'], 'type': 'line', 'name': 'Coal'},
                {'x': df['Unnamed: 0'], 'y': df['Gas'], 'type': 'line', 'name': 'Gas'},
                {'x': df['Unnamed: 0'], 'y': df['Hydroelectricity'], 'type': 'line', 'name': 'Hydroelectricity'},
                {'x': df['Unnamed: 0'], 'y': df['Nuclear'], 'type': 'line', 'name': 'Nuclear'},
                {'x': df['Unnamed: 0'], 'y': df['Biomass and Waste'], 'type': 'line', 'name': 'Biomass and Waste'},
                {'x': df['Unnamed: 0'], 'y': df['Wind'], 'type': 'line', 'name': 'Wind'},
                {'x': df['Unnamed: 0'], 'y': df['Fuel Ethanol'], 'type': 'line', 'name': 'Fuel Ethanol'},
                {'x': df['Unnamed: 0'], 'y': df['Geothermal'], 'type': 'line', 'name': 'Geothermal'},
                {'x': df['Unnamed: 0'], 'y': df['Solar, Tide, Wave, Fuel Cell'], 'type': 'line', 'name': 'Solar, Tide, Wave, Fuel Cell'},
                {'x': df['Unnamed: 0'], 'y': df['Biodiesel'], 'type': 'line', 'name': 'Biodiesel'},
            ],
            'layout': {
                'title': 'Primary energy consumption of the country',
                'xaxis': {'title': 'Date / 30 years'},
                'yaxis': {'title': 'Mtoe'},
            }
        }
    )
            

################
# page gdp-pop #
################
gdp_pop_layout = html.Div([
    dcc.Link('Go back to Country', href='/country'),
    html.Br(),
    html.H1('Choice a country for see the GDP and the population at 2020'),
    dcc.Dropdown(
        id="gdp-pop-dropdown",
        options=[
                {"label": country, "value": country} for country in dfPibPays["Country Name"].unique()
            ],
    ),
    html.Br(),
    html.Div(id="report-gdp-pop"),
], style = {'text-align': 'center'})
@callback(Output('report-gdp-pop', 'children'), [Input('gdp-pop-dropdown', 'value')])
def displayGDPandPopulation(country):
    if country is None:
        return 'Please select a country'
    else:
        return html.Div([
            html.H3(country),
            html.H4("GDP : " + str(dfPibPays.loc[dfPibPays["Country Name"] == country, "2020"].values[0]) + "$"),
            html.H4("Population : " + str(dfPopulationPays.loc[dfPopulationPays["Country Name"] == country, "2020"].values[0]) + " people"),
        ])


#########################
# page carbon-footprint #
#########################
def selectLineOfCountryInDf(df, country):
    return df.loc[df["Country Name"] == country]
dfFrance = selectLineOfCountryInDf(dfEmpreinteCarbone, "France")
dfDenmark = selectLineOfCountryInDf(dfEmpreinteCarbone, "Danmark")
dfCoteIvoire = selectLineOfCountryInDf(dfEmpreinteCarbone, "Côte d'Ivoire")
dfChina = selectLineOfCountryInDf(dfEmpreinteCarbone, "Chine")
dfIndia = selectLineOfCountryInDf(dfEmpreinteCarbone, "Inde")
dfUnitedStates = selectLineOfCountryInDf(dfEmpreinteCarbone, "États-Unis")
carbon_footprint_layout = html.Div([
    dcc.Link('Go back to Country', href='/country'),
    html.Br(),
    html.H1('Choice a country for see the carbon footprint at 2014'),
    dcc.Dropdown(
        id="carbon-footprint-dropdown",
        options=[
                {"label": country, "value": country} for country in dfEmpreinteCarbone["Country Name"].unique()
            ],
    ),
    html.Br(),
    html.Div(id="report-carbon-footprint"),
    html.Br(),
    html.H1('A diagram of the countries where you are established :'),
    dcc.Graph(
        figure = {
            'data': [
                {'x': dfFrance['Country Name'], 'y': dfFrance['2014'], 'type': 'bar', 'name': 'Carbon footprint of France at 2014'},
                {'x': dfDenmark['Country Name'], 'y': dfDenmark['2014'], 'type': 'bar', 'name': 'Carbon footprint of Denmark at 2014'},
                {'x': dfCoteIvoire['Country Name'], 'y': dfCoteIvoire['2014'], 'type': 'bar', 'name': 'Carbon footprint of Cote d\'Ivoire at 2014'},
                {'x': dfChina['Country Name'], 'y': dfChina['2014'], 'type': 'bar', 'name': 'Carbon footprint of China at 2014'},
                {'x': dfIndia['Country Name'], 'y': dfIndia['2014'], 'type': 'bar', 'name': 'Carbon footprint of India at 2014'},
                {'x': dfUnitedStates['Country Name'], 'y': dfUnitedStates['2014'], 'type': 'bar', 'name': 'Carbon footprint of United States at 2014'},
            ],
        }
    ),

], style = {'text-align': 'center'})
@callback(Output('report-carbon-footprint', 'children'), [Input('carbon-footprint-dropdown', 'value')])
def displayCarbonFootprint(value):
    if value is None:
        return 'Please select a country'
    else:
        return html.Div([
            html.H3(value),
            html.H4("Carbon footprint : " + str(dfEmpreinteCarbone.loc[dfEmpreinteCarbone["Country Name"] == value, "2014"].values[0]) + " kg CO2e"),
        ])

#################################
# page carbon-footprint 30 years#
#################################
dfFrance = selectLineOfCountryInDf(dfEmpreinteCarone30years, "France")
fig = go.Figure(data=[go.Scatter(x=dfFrance['Country Name'], y=dfFrance['2014'], name='Carbon footprint of France at 2014')])
carbon_footprint_30years_layout = html.Div([
    dcc.Link('Go back to Country', href='/country'),
    html.Br(),
    html.H1('Choice a country for see the evolutions of carbon'),
    html.Br(),
    dcc.Graph(
        figure = fig
    )
], style = {'text-align': 'center'})

################################
# page carbon-footprint-global #
################################


fig = px.pie(dfEmpreinteCarbone, values='2014', names='Country Name', title='Population')

carbon_footprint_global_layout = html.Div([
    dcc.Link('Go back to Country', href='/country'),
    html.Br(),
    html.H1('Choice a country to compare '),
    dcc.Dropdown(
        id="carbon-footprint-global-dropdown",
        options=[
                {"label": country, "value": country} for country in dfEmpreinteCarbone["Country Name"].unique()
            ],
    ),
    dcc.Graph(
        figure = fig
    ),
    html.Div(id="report-carbon-footprint-global"),
], style = {'text-align': 'center'})
@callback(Output('report-carbon-footprint-global', 'children'), [Input('carbon-footprint-global-dropdown', 'value')])
def compareCarbonFootprint(country):
    return px.pie(dfEmpreinteCarbone, values='2014', names='Country Name', title='Population')
    
    
    


############
# page map #
############
map_layout = html.Div([
    html.H1('Map'),
    html.Br(),
    dcc.Link('Sea level rise forecasts between 2081 and 2100', href='/sea-level'),
    html.Br(),
    html.Br(),
    dcc.Link('World temperature forecasts from 2041 to 2060', href='/temperature'),
    html.Br(),
    html.Br(),
    dcc.Link('Go back to home', href='/')
], style = {'text-align': 'center'})
@callback(Output('map-content', 'children'),
              [Input('map-radios', 'value')])
def map_radios(value):
    return f'You have selected {value}'

##################
# page sea level #
##################
fig = px.choropleth_mapbox(dfSeaLevel, geojson=counties, locations='pays', featureidkey="properties.iso_a3", color='total',
                           color_continuous_scale="Viridis",mapbox_style="carto-positron",
                           )

fig2 = px.bar(dfAverageTemperature, x='country', y='values', color='values', barmode="group")

sea_level_layout = html.Div([
    dcc.Link('Go back to Map', href='/map'),
    html.Br(),
    html.H1(children='Map of rising waters by country'),
    html.H4(children = 'Zoom in and out with your mouse wheel'),
    html.Div(children='''
        This data was provided by the UPCC.
    '''),
    dcc.Graph(
        id='Map ocean',
        figure=fig
    ),
], style = {'text-align': 'center'})

####################
# page temperature #
####################
fig3 = px.choropleth_mapbox(dfTemperatureForecast, geojson=counties, locations='pays', featureidkey="properties.iso_a3", color='tas_anom',
                           color_continuous_scale="Viridis",mapbox_style="carto-positron",
                           )
temperature_layout = html.Div([
    dcc.Link('Go back to Map', href='/map'),
    html.Br(),
    html.H2(children='Average temperature evolution diagram from 2041 - 2060 based on 1995 - 2014'),
    html.Div(children='''
        This data was provided by ipcc.
    '''),
    html.H4(children = 'Zoom in and out with your mouse wheel'),
    dcc.Graph(
        id='Average Temperature',
        figure=fig3
    ),
    html.H2(children='Temperature increase map from 2041 to 2060 '),
    html.Div(children='''
        This data was provided by UPCC.
    '''),
    
    dcc.Graph(
        id='TemperatureCountry',
        figure=fig2
    )
], style = {'text-align': 'center'})

# Update the index
@callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/country':
        return country_layout
    elif pathname == '/map':
        return map_layout
    elif pathname == '/primary-energy':
        return primary_energy_layout
    elif pathname == '/gdp-pop':
        return gdp_pop_layout
    elif pathname == '/carbon-footprint':
        return carbon_footprint_layout
    elif pathname == '/carbon-footprint-30':
        return carbon_footprint_30years_layout
    elif pathname == '/carbon-footprint-global':
        return carbon_footprint_global_layout
    elif pathname == '/temperature':
        return temperature_layout
    elif pathname == '/sea-level':
        return sea_level_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


if __name__ == '__main__':
    app.run_server(debug=True)