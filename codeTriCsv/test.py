import csv
from sqlite3 import Row
from numpy import NaN
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
import pycountry_convert as pc

countrys = ["France","Denmark","Germany","Italy","United States","China","India"]
pd.set_option('mode.chained_assignment', None)





# Niveau de la mer
#carte
LevelMer = pd.read_csv("NiveauMer.csv")




def callCityStateCountry(FileName):
    df = pd.read_csv(FileName)
    allValues = ""
    for i in df.index:
        latitude = df.loc[i,"lat"]
        longitude = df.loc[i,"lon"]
        total = df.loc[i,"total"]
        city, state , country = city_state_country(df.loc[i],latitude,longitude)
        print(country)
        if country != None and total != NaN:
            country_code = pc.country_name_to_country_alpha2(country, cn_name_format="default")
            continent_name = pc.country_alpha2_to_continent_code(country_code)
            allValues += str(latitude) + "," + str(longitude) +  "," + str(continent_name) + "," + str(country) + "," + str(city) + ","+ str(total) + "\n"
    print(allValues)
    df2 = df(allValues)
    return df2              
        
def city_state_country(row,lat,lon):
    geolocator = Nominatim(user_agent="myGeocoder")
    string_value = str(lat) + "," + str(lon)
    location = geolocator.reverse(string_value, exactly_one=True,language='en')
    if location==None:
        row['city'], row['state'], row['country2'] = None, None, None
        return None, None, None
    address = location.raw['address']
    city = address.get('city', '')
    state = address.get('state', '')
    country = address.get('country', '')
    return city, state , country

callCityStateCountry("NiveauMer.csv") 