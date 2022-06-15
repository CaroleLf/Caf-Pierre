import dash as dcc
from dash import html
import plotly.express as px
import pandas as pd

from csv import writer
from csv import reader

#Method make the average for each country
def average(fileName):
    country = {"France": 0 , "Denmark": 0, "Germany": 0, "Italy": 0, "United States": 0, "China" : 0,"India": 0 }
    countryNumber = {"France": 0 , "Denmark": 0, "Germany": 0, "Italy": 0, "United States": 0, "China" : 0,"India": 0 }
    df = pd.read_csv(fileName)
    for i in range(len(df)):
        for j in range(len(country)):
            if df.iloc[i]["country"] == list(country.keys())[j]:
                country[list(country.keys())[j]] += df.iloc[i]["values"]
                countryNumber[list(countryNumber.keys())[j]] += 1
    for i in range(len(country)):
        if countryNumber[list(countryNumber.keys())[i]] != 0:
            country[list(country.keys())[i]] = country[list(country.keys())[i]]/countryNumber[list(countryNumber.keys())[i]]
    
    df = pd.DataFrame.from_dict(country, orient='index')
    csv = pd.DataFrame.to_csv(df)
    with open("averageTemperature.csv", 'a') as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in country:
            writer.writerow([val])
    return csv


import pandas as pd


df = pd.read_csv("LatLonPays.csv")
Pays  = df["Pays"]
df1 = pd.read_csv("NiveauMer.csv")
df1["pays"] = Pays
df1.to_csv("sample.csv", index=False)


#method delete the row null for the Pays columns
def deleteNull(fileName):
    df = pd.read_csv(fileName)
    df = df.dropna(subset=["pays"])
    df = df.dropna(subset=["total"])
    del df["crs"]
    df.to_csv("newNiveauMer.csv", index=False)

deleteNull("sample.csv")