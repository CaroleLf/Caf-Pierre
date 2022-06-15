import csv
import pandas as pd
import geopy
from geopy.geocoders import Nominatim
import pycountry_convert as pc



geolocator = Nominatim(user_agent="geoapiExercises")

countrys = ["France","Denmark","Germany","Italy","United States","China","India"]
pd.set_option('mode.chained_assignment', None)


locator = Nominatim(user_agent="myGeocoder")

"""""
def displayTownAndCountry(fileName):
    df = pd.read_csv(fileName)
    df = df.iloc[44466:] 
    for i in df.index:
        latitude = df.loc[i,"latitude"]
        longitude = df.loc[i,"longitude"]
        geolocator = Nominatim(user_agent="http")
        string_value = str(latitude) + "," + str(longitude)
        location = geolocator.reverse(string_value, exactly_one=True,language='en')
        address = location.row['address']
        city = address.get('city', '')
        state = address.get('state', '')
        country = address.get('country', '')
        print(city, state, country)


      
        27.5 119.5



"""
def callCityStateCountry(FileName):
    df = pd.read_csv(FileName)
    allValues = []
    df = df.iloc[41528:]
    for i in df.index:
        latitude = df.loc[i,"lat"]
        longitude = df.loc[i,"lon"]
        values = df.loc[i,"total"]
        print(values)
        print(latitude,longitude)
        if values!="nan" :
                      city,state , country = city_state_country(df.loc[i],latitude,longitude)

        if country != None:
            print(country)
            print(latitude,longitude)
            for i in range(len(countrys)):
                    if country == countrys[i]:
                        with open('finalValuesNiveauMer.csv','a') as f:
                            country_code = pc.country_name_to_country_alpha2(country, cn_name_format="default")
                            continent_name = pc.country_alpha2_to_continent_code(country_code)
                            writer = csv.writer(f)
                            writer.writerow([latitude,longitude,country,continent_name,values,city])

    











def city_state_country(row,lat,lon):
    geolocator = Nominatim(user_agent="https")
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





        

"""""
def createCsvFile():
    df = pd.read_csv("CMIP6.csv")
    df = df.iloc[53477:]
    for i in df.index:
        latitude = df.loc[i,"latitude"]
        longitude = df.loc[i,"longitude"]
        data  = df.loc[i,"tas_anom"]
        print(latitude, longitude, data)
        with open('CMIP6-values.csv','a') as f:
            writer = csv.writer(f)
            if(location != None):
                print("Test")
                print(latitude, longitude)
                print(location)
                writer.writerow([latitude, longitude, data,location])



def LocationOrNull(fileName):
    df = pd.read_csv(fileName)
    df = df.iloc[30000:] 

    for i in df.index:
        latitude = df.loc[i,"latitude"]
        longitude = df.loc[i,"longitude"]
        print(latitude, longitude)
        location = getplace(latitude, longitude)
        return location
"""

#callCityStateCountry("niveauMer")



#Method make the average for each country
def average(fileName):
    country = {"France": 0 , "Denmark": 0, "Germany": 0, "Italy": 0, "United States": 0, "China" : 0,"India": 0 }
    countryNumber = {"France": 0 , "Denmark": 0, "Germany": 0, "Italy": 0, "United States": 0, "China" : 0,"India": 0 }
    df = pd.read_csv(fileName)
    for i in range(len(df)):
        for j in range(len(country)):
            print(df.iloc[i]["country"])
            print(list(country.keys())[j])
            if df.iloc[i]["country"] == list(country.keys())[j]:
                country[list(country.keys())[j]] += df.iloc[i]["values"]
                countryNumber[list(countryNumber.keys())[j]] += 1
                print(country)
    for i in range(len(country)):
        if countryNumber[list(countryNumber.keys())[i]] != 0:
            country[list(country.keys())[i]] = country[list(country.keys())[i]]/countryNumber[list(countryNumber.keys())[i]]
    
    df = pd.DataFrame.from_dict(country, orient='index')
    df.to_csv("average.csv")
    print(df)


average("finalValuesTemperature")


