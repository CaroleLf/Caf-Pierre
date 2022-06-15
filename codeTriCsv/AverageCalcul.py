from operator import index
from traceback import print_tb
from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd


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
                print(country)
    for i in range(len(country)):
        if countryNumber[list(countryNumber.keys())[i]] != 0:
            country[list(country.keys())[i]] = country[list(country.keys())[i]]/countryNumber[list(countryNumber.keys())[i]]
    
    df = pd.DataFrame.from_dict(country, orient='index')
    print(df)


average("finalValuesTemperature.csv")
