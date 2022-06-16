from dash import Dash, dcc, Output, Input,html  # pip install dash
import dash_bootstrap_components as dbc
from numpy import NaN    # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd     
import csv

df = pd.read_csv("empreinte_carbone.csv")

# Build your components
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
mytitle = dcc.Markdown(children='')
mygraph = dcc.Graph(figure={})

date=['1960','1961','1962','1963','1964','1965','1966','1967','1968','1969','1970','1971','1972','1973','1974','1975','1976','1977','1978','1979','1980','1981','1982','1983','1984','1985','1986','1987','1988','1989','1990','1991','1992','1993','1994','1995','1996','1997','1998','1999','2000',
	'2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021'
]

colors = {
    'background': '#111111',
    'text': '#000000'
}
# Customize your own Layout
  

app.layout = html.Div([
    html.H1(
        children='Emprunte carbone sur 30 ans',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
     dcc.Dropdown(
                df['CountryName'].unique(),
                id='xaxis-column'
            ),
    html.Div(id="report"),
])




# Callback allows components to interact
@app.callback(
    Output(component_id='report', component_property='children'),
    Input(component_id='xaxis-column', component_property='value'),
)

#recup the value 

def update_country(value):
    if value is None:
        return 'Please select a country'
    else:
        getValueForaCountry(value)
        df = pd.read_csv("EmpreinteCarbone30years{value}.csv")
        fig = px.line(df, x='year', y='value')
        return html.Div([
            html.H3('Empreinte carbonne de : '+ value + ' sur 30 ans '), 
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
    for i in df.index:
        if df.loc[i, 'CountryName'] == value:
            for j in date:
                if isNaN(df.loc[i, j]):
                    valueTab[j] = 0
                else:
                    valueTab[j] = (df.loc[i, j])
    print(valueTab)
    with open('EmpreinteCarbone30years{value}.csv', 'a') as f:
        key_list = list(valueTab.keys())
        val_list = list(valueTab.values())
        writer = csv.writer(f)
        writer.writerow(['year', 'value'])
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
        value  = df.loc[i, 'value']
        if value == 0:
            df.drop(i, inplace=True)
    df.to_csv("EmpreinteCarbone30years{value}.csv", index=False)



# Run app
if __name__=='__main__':
    app.run_server(debug=True, port=8054)