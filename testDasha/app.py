from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd

dfPibPays = pd.read_csv("pib.csv", usecols=['Country Name', '2020'])
dfPopulationPays = pd.read_csv("pop_totale.csv", usecols=['Country Name', '2020'])
dfPrimaryEnergy = pd.read_csv("primary_energy.csv", usecols=['Country Name','2014'])
print(dfPibPays)
print(dfPrimaryEnergy)

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
    dcc.Dropdown(
        id='primary-dropdown',
        options=[{'label': i, 'value': i} for i in dfPrimaryEnergy['Country Name'].unique()],
    ),
    html.Br(),
    html.Div(id="report-primary-energy"),
], style = {'text-align': 'center'})
@callback(Output('report-primary-energy', 'children'), [Input('primary-dropdown', 'value')])
def show_primary_energy(country):
    if country is None:
        return 'Please select a country'
    else:
        return html.Div([
            html.H3(country),
            html.H4('Primary energy consumption : '+ str(dfPrimaryEnergy.loc[dfPrimaryEnergy['Country Name'] == country, '2014'].values[0]) + ' GWh'),
            ])
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