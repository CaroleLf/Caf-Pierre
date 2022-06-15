from gc import callbacks
from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import matplotlib.pyplot as plt

#############################################################################################################################

dfPibPays = pd.read_csv("pib.csv", usecols=['Country Name', '2020'])
dfPopulationPays = pd.read_csv("pop_totale.csv", usecols=['Country Name', '2020'])

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

penergyfrance = pd.read_csv("primary_energy/primary_energy_france.csv", sep=';')
penergyfrance = setDateVoulue(penergyfrance)

penergychina = pd.read_csv("primary_energy/primary_energy_china.csv", sep=';')
penergychina = setDateVoulue(penergychina)

penergycoteivoire = pd.read_csv("primary_energy/primary_energy_coteivoire.csv", sep=';')
penergycoteivoire = setDateVoulue(penergycoteivoire)

penergyindia = pd.read_csv("primary_energy/primary_energy_india.csv", sep=';')
penergyindia = setDateVoulue(penergyindia)

penergydenmark = pd.read_csv("primary_energy/primary_energy_denmark.csv", sep=';')
penergydenmark = setDateVoulue(penergydenmark)

penergyunitedstates = pd.read_csv("primary_energy/primary_energy_unitedstates.csv", sep=';')
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
    dcc.Link('Go to Country', href='/country'),
    html.Br(),
    html.Br(),
    dcc.Link('Go to Map', href='/map'),
], style = {'text-align': 'center'})

################
# page country #
################
country_layout = html.Div([
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
                'yaxis': {'title': 'Primary energy consumption'},
            }
        }
    )
            

#'The primary energy consumption of {} is {}'.format(country, dfPrimaryEnergy.loc[dfPrimaryEnergy['Country Name'] == country, '2014'].values[0])


################
# page gdp-pop #
################
gdp_pop_layout = html.Div([
    dcc.Link('Go back to Country', href='/country'),
    html.Br(),
    html.H1('Choice a country for see the GDP and the population'),
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


############
# page map #
############
map_layout = html.Div([
    html.H1('Map'),
    dcc.RadioItems(['Orange', 'Blue', 'Red'], 'Orange', id='map-radios'),
    html.Div(id='map-content'),
    html.Br(),
    dcc.Link('Go to Country', href='/country'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
], style = {'text-align': 'center'})

@callback(Output('map-content', 'children'),
              [Input('map-radios', 'value')])
def map_radios(value):
    return f'You have selected {value}'


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
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


if __name__ == '__main__':
    app.run_server(debug=True)