from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px
import geopandas as gpd
import csv
import sqlite3
from os import path
conn = sqlite3.connect(path.dirname(__file__).replace("/application","") + "/CoffeePierre.db")
c = conn.cursor()

#############################################################################################################################
queryPibPays = '''SELECT nomRégion as 'Country Name', PIB as '2020' FROM Région join PIB on PIB.idRégion = Région.idRégion where année = '2020' '''
dfPibPays = pd.read_sql(queryPibPays, conn)
queryHabitantsPays = '''SELECT nomRégion as 'Country Name', nbHabitant as '2020' FROM Région join Habitants on Habitants.idRégion = Région.idRégion where année = '2020' '''
dfPopulationPays = pd.read_sql(queryHabitantsPays, conn)
dfEmpreinteCarbone = pd.read_csv(path.dirname(__file__) + "/csv/empreinte_carbone.csv", usecols=['Country Name', '2014'])
dfEmpreinteCarone30years = pd.read_csv(path.dirname(__file__) + "/csv/empreinte_carbone.csv")
dfSeaLevel = pd.read_csv(path.dirname(__file__) + "/csv/NiveauMerUpdate.csv")
dfTemperatureForecast = pd.read_csv(path.dirname(__file__) + "/csv/AllTemperatureMean2041-2060Pays.csv")
dfAverageTemperature = pd.read_csv(path.dirname(__file__) + "/csv/AverageTemperature1941-1960.csv")
counties = gpd.read_file(path.dirname(__file__) + "/custom.geo.json")
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
    html.H1('Country'),
    html.Br(),
    dcc.Link('Display the primary energy consumption by sector of a country', href='/primary-energy'),
    html.Br(),
    html.Br(),
    dcc.Link('Display the GES by sector of a country', href='/ges'),
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

queryPenergyFrance = '''SELECT année as 'Unnamed: 0', Oil, Coal, Gas, Hydroelectricity, Nuclear, "Biomass and Waste", Wind, "Fuel Ethanol",  "Solar, Tide, Wave, Fuel Cell", Geothermal, Biodiesel FROM 'Primary Energies' where nomRégion = 'France' and année > 1985 and année <2017  '''
penergyfrance = pd.read_sql(queryPenergyFrance, conn)


queryPenergyChina = '''SELECT année as 'Unnamed: 0', Oil, Coal, Gas, Hydroelectricity, Nuclear, "Biomass and Waste", Wind, "Fuel Ethanol",  "Solar, Tide, Wave, Fuel Cell", Geothermal, Biodiesel FROM 'Primary Energies' where nomRégion = 'China' and année > 1985 and année <2017  '''
penergychina = pd.read_sql(queryPenergyChina, conn)

queryPenergycoteivoire = '''SELECT année as 'Unnamed: 0', Oil, Coal, Gas, Hydroelectricity, Nuclear, "Biomass and Waste", Wind, "Fuel Ethanol",  "Solar, Tide, Wave, Fuel Cell", Geothermal, Biodiesel FROM 'Primary Energies' where nomRégion = 'Cote d''Ivoire' and année > 1985 and année <2017  '''
penergycoteivoire = pd.read_sql(queryPenergycoteivoire, conn)


queryPenergyIndia = '''SELECT année as 'Unnamed: 0', Oil, Coal, Gas, Hydroelectricity, Nuclear, "Biomass and Waste", Wind, "Fuel Ethanol",  "Solar, Tide, Wave, Fuel Cell", Geothermal, Biodiesel FROM 'Primary Energies' where nomRégion = 'India' and année > 1985 and année <2017  '''
penergyindia = pd.read_sql(queryPenergyIndia, conn)

queryPenergyDenmark = '''SELECT année as 'Unnamed: 0', Oil, Coal, Gas, Hydroelectricity, Nuclear, "Biomass and Waste", Wind, "Fuel Ethanol",  "Solar, Tide, Wave, Fuel Cell", Geothermal, Biodiesel FROM 'Primary Energies' where nomRégion = 'Denmark' and année > 1985 and année <2017  '''
penergydenmark = pd.read_sql(queryPenergyDenmark, conn)


queryPenergyUnitedstates = '''SELECT année as 'Unnamed: 0', Oil, Coal, Gas, Hydroelectricity, Nuclear, "Biomass and Waste", Wind, "Fuel Ethanol",  "Solar, Tide, Wave, Fuel Cell", Geothermal, Biodiesel FROM 'Primary Energies' where nomRégion = 'United States' and année > 1985 and année <2017  '''
penergyunitedstates = pd.read_sql(queryPenergyUnitedstates, conn)


queryPenergyGermany = '''SELECT année as 'Unnamed: 0', Oil, Coal, Gas, Hydroelectricity, Nuclear, "Biomass and Waste", Wind, "Fuel Ethanol",  "Solar, Tide, Wave, Fuel Cell", Geothermal, Biodiesel FROM 'Primary Energies' where nomRégion = 'Germany' and année > 1985 and année <2017  '''
penergygermany = pd.read_sql(queryPenergyGermany, conn)

primary_energy_layout = html.Div([
    dcc.Link('Go back to Country', href='/country'),
    html.Br(),
    html.H1('Choose to see the primary energy consumption of a country'),
    html.Br(),
    dcc.Dropdown(["France", "Denmark", "Cote d'Ivoire", "China", "India", "United States", "Germany"], id='country-dropdown'),
    html.Br(),
    html.Div(id="report-primary-energy"),
], style = {'text-align': 'center'})
@callback(Output('report-primary-energy', 'children'), Input('country-dropdown', 'value'))
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
    if value == "Germany":
        df = penergygermany
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



############
# page ges #
############
queryGhouseGasFrance = '''SELECT année as 'Unnamed: 0', Energy, Agriculture, "Industry and Construction", Waste, "Other Sectors" FROM 'Greenhouse Gas' where nomRégion = 'France' and année > 1985 and année <2017  '''
ghousegas_france = pd.read_sql(queryGhouseGasFrance, conn)

queryGhouseGasCoteivoire = '''SELECT année as 'Unnamed: 0', Energy, Agriculture, "Industry and Construction", Waste, "Other Sectors" FROM 'Greenhouse Gas' where nomRégion = 'Cote d''Ivoire' and année > 1985 and année <2017  '''
ghousegas_coteivoire = pd.read_sql(queryGhouseGasCoteivoire, conn)

queryGhouseDenmark = '''SELECT année as 'Unnamed: 0', Energy, Agriculture, "Industry and Construction", Waste, "Other Sectors" FROM 'Greenhouse Gas' where nomRégion = 'Denmark' and année > 1985 and année <2017  '''
ghousegas_denmark = pd.read_sql(queryGhouseDenmark, conn)

queryGhouseGasChina = '''SELECT année as 'Unnamed: 0', Energy, Agriculture, "Industry and Construction", Waste, "Other Sectors" FROM 'Greenhouse Gas' where nomRégion = 'China' and année > 1985 and année <2017  '''
ghousegas_china = pd.read_sql(queryGhouseGasChina, conn)

queryGhouseGasInde = '''SELECT année as 'Unnamed: 0', Energy, Agriculture, "Industry and Construction", Waste, "Other Sectors" FROM 'Greenhouse Gas' where nomRégion = 'India' and année > 1985 and année <2017  '''
ghousegas_inde = pd.read_sql(queryGhouseGasInde, conn)

queryGhouseGasUnitedStates = '''SELECT année as 'Unnamed: 0', Energy, Agriculture, "Industry and Construction", Waste, "Other Sectors" FROM 'Greenhouse Gas' where nomRégion = 'United States' and année > 1985 and année <2017  '''
ghousegas_unitedstates = pd.read_sql(queryGhouseGasUnitedStates, conn)


queryGhouseGasGermany = '''SELECT année as 'Unnamed: 0', Energy, Agriculture, "Industry and Construction", Waste, "Other Sectors" FROM 'Greenhouse Gas' where nomRégion = 'Germany' and année > 1985 and année <2017  '''
ghousegas_germany = pd.read_sql(queryGhouseGasGermany, conn)

ges_layout = html.Div([
    dcc.Link('Go back to Country', href='/country'),
    html.Br(),
    html.H1('Choose to see the greenhouse gas production of a country'),
    html.Br(),
    dcc.Dropdown(["France", "Cote d'Ivoire", "Denmark", "China", "India", "United States", "Germany"], id='country-dropdown'),
    html.Br(),
    html.Div(id="report-ghouse-gas"),
], style = {'text-align': 'center'})
@callback(Output('report-ghouse-gas', 'children'), Input('country-dropdown', 'value'))
def retGraphGreenhouseGas(value):
    if value == "France":
        df = ghousegas_france
    if value == "Cote d'Ivoire":
        df = ghousegas_coteivoire
    if value == "Denmark":
        df = ghousegas_denmark
    if value == "China":
        df = ghousegas_china
    if value == "India":
        df = ghousegas_inde
    if value == "United States":
        df = ghousegas_unitedstates
    if value == "Germany":
        df = ghousegas_germany

    return dcc.Graph(
        figure = {
            'data': [
                {'x': df['Unnamed: 0'], 'y': df['Energy'], 'type': 'line', 'name': 'Energy'},
                {'x': df['Unnamed: 0'], 'y': df['Agriculture'], 'type': 'line', 'name': 'Agriculture'},
                {'x': df['Unnamed: 0'], 'y': df['Industry and Construction'], 'type': 'line', 'name': 'Industry and Construction'},
                {'x': df['Unnamed: 0'], 'y': df['Waste'], 'type': 'line', 'name': 'Waste'},
                {'x': df['Unnamed: 0'], 'y': df['Other Sectors'], 'type': 'line', 'name': 'Other Sectors'},
            ],
            'layout': {
                'title': 'Greenhouse gas production of the country',
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
    html.H1('Choose to see the GDP and the population in 2020 of a country'),
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
            html.H4("Population : " + str(dfPopulationPays.loc[dfPopulationPays["Country Name"] == country, "2020"].values[0]) + " inhabitants"),
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
dfGermany = selectLineOfCountryInDf(dfEmpreinteCarbone, "Allemagne")
carbon_footprint_layout = html.Div([
    dcc.Link('Go back to Country', href='/country'),
    html.Br(),
    html.H1('Choose to see the carbon footprint in 2014 of a country'),
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
                {'x': dfGermany['Country Name'], 'y': dfGermany['2014'], 'type': 'bar', 'name': 'Carbon footprint of Germany at 2014'},
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

date=['1960','1961','1962','1963','1964','1965','1966','1967','1968','1969','1970','1971','1972','1973','1974','1975','1976','1977','1978','1979','1980','1981','1982','1983','1984','1985','1986','1987','1988','1989','1990','1991','1992','1993','1994','1995','1996','1997','1998','1999','2000',
	'2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021'
]

colors = {
    'background': '#111111',
    'text': '#000000'
}  

carbon_footprint_30years_layout = html.Div([
    html.Div([    
    dcc.Link('Go back to Country', href='/country'),
    html.Br(),
    html.H1(
        children='Carbon footprint of a country over 30 years',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    )], style = {'width' : '100%'}),
    html.Div([
        html.H3(
        children='Choose a country where you are established',
    ),
    dcc.Dropdown(["France", "Danemark", "Côte d'Ivoire", "Chine", "Inde", "États-Unis", "Allemagne"], 
    id='carbon-footprint-30years-paysimplente'),
        html.Div(id="report-carbon-footprint-30years-paysimplente")], style = {'width' : '50%'}),
    html.Div([
         html.H3(
        children='Choose a country in the world',
    ),
    dcc.Dropdown(
                dfEmpreinteCarone30years['Country Name'].unique(),
                id='xaxis-column'
            ),
    html.Div(id="report"),
    ], style = {'width' : '50%'})
], style = {'text-align': 'center', 'display' : 'flex', 'flex-wrap' : 'wrap'})


# Callback allows components to interact
@app.callback(
    Output(component_id='report', component_property='children'),
    Input(component_id='xaxis-column', component_property='value'),
)
@app.callback(
    Output(component_id='report-carbon-footprint-30years-paysimplente', component_property='children'),
    Input(component_id='carbon-footprint-30years-paysimplente', component_property='value'),
)

def update_country(value):
    if value is None:
        return 'Please select a country'
    else:
        getValueForaCountry(value)
        df = pd.read_csv("EmpreinteCarbone30years{value}.csv")
        fig = px.line(df, x='Year', y='KTO2e')
        return html.Div([
            html.H3('Carbon footprint of : '+ value + ' over 30 years'),
            dcc.Graph(     
                figure = fig
            )
        ])


def isNaN(num):
    return num != num

def getValueForaCountry(value):
    f = open("EmpreinteCarbone30years{value}.csv", "w")
    f.truncate()
    f.close()
    valueTab = {'1960' : 0 ,'1961' : 0,'1962' : 0 ,'1963': 0,'1964': 0,'1965': 0 ,'1966' : 0,'1967' : 0,'1968' :  0,'1969' : 0,'1970' : 0 ,'1971' : 0,'1972' : 0 ,'1973' : 0 ,'1974' : 0 ,'1975' : 0,'1976' : 0,'1977' : 0 ,'1978' : 0 ,'1979' : 0 ,'1980': 0, '1981': 0,'1982': 0,'1983': 0,'1984': 0,'1985': 0,'1986': 0,'1987': 0,'1988': 0, '1989' : 0 ,'1990' : 0 ,'1989': 0,'1991': 0,'1992': 0,'1993': 0,'1994': 0,'1995': 0,'1996': 0,'1997': 0,'1998': 0,'1999': 0,'2000': 0,
	'2001': 0,'2002': 0,'2003': 0,'2004': 0,'2005': 0,'2006': 0,'2007': 0,'2008': 0,'2009': 0,'2010': 0,'2011': 0,'2012': 0,'2013': 0,'2014': 0,'2015': 0,'2016': 0,'2017': 0,'2018': 0 ,'2019': 0,'2020': 0,'2021': 0}
    for i in dfEmpreinteCarone30years.index:
        if dfEmpreinteCarone30years.loc[i, 'Country Name'] == value:
            for j in date:
                if isNaN(dfEmpreinteCarone30years.loc[i, j]):
                    valueTab[j] = 0
                else:
                    valueTab[j] = (dfEmpreinteCarone30years.loc[i, j])
    with open('EmpreinteCarbone30years{value}.csv', 'a') as f:
        key_list = list(valueTab.keys())
        val_list = list(valueTab.values())
        writer = csv.writer(f)
        writer.writerow(['Year', 'KTO2e'])
        i = 0
        j = 0
        while j < len(key_list)-1 and i < len(val_list)-1:
            writer.writerow([key_list[j], val_list[i]])
            i += 1
            j += 1
    deleteNull("EmpreinteCarbone30years{value}.csv")
        

def deleteNull(fileName):
    df = pd.read_csv(fileName)
    for i in df.index:
        value  = df.loc[i, 'KTO2e']
        if value == 0:
            df.drop(i, inplace=True)
    df.to_csv("EmpreinteCarbone30years{value}.csv", index=False)

################################
# page carbon-footprint-global #
################################

def paysVoulus(pays):
    return [pays, "Monde"]

carbon_footprint_global_layout = html.Div([
    html.Div([
        dcc.Link('Go back to Country', href='/country'),
        html.H1('The carbon footprint at 2014'),
        html.H1('Choose a country to compare')
        ], style = {'width' : '100%'}),
    html.Br(),
    html.Div([
        html.H1('Countries where you are establised '),
        dcc.Dropdown(["France", "Danemark", "Côte d'Ivoire", "Chine", "Inde", "États-Unis", "Allemagne"], id='carbon-footprint-global-paysimplente'),
        html.Div(id="report-carbon-footprint-global-paysimplente"),
    ], style = {'width': '50%',}),
    
    html.Div([
    html.H1('Countries in the world'),
    dcc.Dropdown(
        id="carbon-footprint-global-dropdown",
        options=[
                {"label": country, "value": country} for country in dfEmpreinteCarbone["Country Name"].unique()
            ],
    ),
    html.Div(id="report-carbon-footprint-global"),
    ], style = {'width': '50%'}),
    
], style = {'text-align': 'center', 'display' : 'flex', 'flex-wrap' : 'wrap'})
@callback(Output('report-carbon-footprint-global-paysimplente', 'children'), [Input('carbon-footprint-global-paysimplente', 'value')])
def compareCarbonFootprint(country):
    paysVoulusA = paysVoulus(country)
    df = dfEmpreinteCarbone[dfEmpreinteCarbone["Country Name"].isin(paysVoulusA)]
    return dcc.Graph(figure = px.pie(df, values='2014', names='Country Name', title='The carbon footprint at 2014'))

@callback(Output('report-carbon-footprint-global', 'children'), [Input('carbon-footprint-global-dropdown', 'value')])
def compareCarbonFootprint(country):
    paysVoulusA = paysVoulus(country)
    df = dfEmpreinteCarbone[dfEmpreinteCarbone["Country Name"].isin(paysVoulusA)]
    return dcc.Graph(figure = px.pie(df, values='2014', names='Country Name', title='The carbon footprint at 2014'))


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
    dcc.Link('Activity with the most carbon footprint', href='/activity'),
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
                           color_continuous_scale="Viridis",mapbox_style="carto-positron", zoom = 0,width=1000,height=1000
                           )

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
        figure=fig,
        style = {'margin-left' : '22%'}
    ),
], style = {'text-align': 'center'})

####################
# page temperature #
####################
fig2 = px.bar(dfAverageTemperature, x='country', y='values', color='values', barmode="group")

fig3 = px.choropleth_mapbox(dfTemperatureForecast, geojson=counties, locations='pays', featureidkey="properties.iso_a3", color='total',
                           color_continuous_scale="Viridis",mapbox_style="carto-positron", zoom = 0,width=1000,height=1000
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
        figure=fig3,
        style = {'margin-left' : '22%'}
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

#################
# page activity #
#################
queryActivityFootprint = ''' SELECT nomActivité as 'Sector', empreinte as 'Empreinte carbone en MtCO2' FROM Activité '''
dfActivityFootprint = pd.read_sql(queryActivityFootprint, conn)

fig =px.pie(dfActivityFootprint, values='Empreinte carbone en MtCO2', names='Sector', title='Carbone footprint by sector')

activity_layout = html.Div([
    dcc.Link('Go back to Map', href='/map'),
    html.Br(),
    html.H1(
        children='Activity with the most carbon footprint',
    ),
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig
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
    elif pathname == '/ges':
        return ges_layout
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
    elif pathname == '/activity':
        return activity_layout
    else:
        return index_page

if __name__ == '__main__':
    app.run_server()