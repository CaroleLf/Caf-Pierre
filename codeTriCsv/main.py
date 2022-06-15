import csv
import pandas as pd
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from pyrsistent import l

geolocator = Nominatim(user_agent="geoapiExercises")

locator = Nominatim(user_agent="myGeocoder")


def displayTownAndCountry(fileName):
    df = pd.read_csv(fileName)
    df = df.iloc[30000:]
    for i in df.index:
        latitude = df.loc[i, "latitude"]
        longitude = df.loc[i, "longitude"]
        print(latitude, longitude)
        location = getplace(latitude, longitude)
        print(location)


def getplace(lat, lon):
    geolocator = Nominatim(user_agent="http")
    string_value = str(lat) + "," + str(lon)
    location = geolocator.reverse(string_value)
    return location


def LocationOrNull(fileName):
    df = pd.read_csv(fileName)
    df = df.iloc[30000:]
    for i in df.index:
        latitude = df.loc[i, "latitude"]
        longitude = df.loc[i, "longitude"]
        print(latitude, longitude)
        location = getplace(latitude, longitude)
        return location


def createCsvFile():
    df = pd.read_csv("CMIP6.csv")
    for i in df.index:
        latitude = df.loc[i, "latitude"]
        longitude = df.loc[i, "longitude"]
        data = df.loc[i, "tas_anom"]
        print(latitude, longitude, data)
        location = getplace(latitude, longitude)
        with open('CMIP6-values.csv', 'a') as f:
            writer = csv.writer(f)
            if (location != None):
                print("Test")
                print(latitude, longitude)
                print(location)
                writer.writerow([latitude, longitude, data, location])


createCsvFile()
