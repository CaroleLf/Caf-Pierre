import pandas as pd 
import plotly.graph_objects as go

df = pd.read_csv("finalValuesTemperature.csv")
df["Text"] = "Country " + df["country"]


fig = go.Figure(data=go.Choropleth(
    lon=df['longitude'],
    lat=df['latitude'],
    colorscale='Blues',
    colorbar=df['values'],
    text = df['Text'] ,
    geoscope='world',
)
)


fig.update_layout(
    title_text='Temperature moyenne des pays',
    geo_scope='world',
)