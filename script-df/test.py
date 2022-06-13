import csv
from sqlite3 import Row
import pandas as pd
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import matplotlib.pyplot as plt
import tqdm
from tqdm._tqdm_notebook import tqdm_notebook
from os import path

pibPays = pd.read_csv(path.dirname(__file__) + "/pib.csv", usecols=['Country Name', '2020'])
populationPays = pd.read_csv(path.dirname(__file__) + "/pop_totale.csv", usecols=['Country Name','2020'])
paysVoulus = ["France", "Denmark", "Cote d'Ivoire", "China", "India", "United States"]
paysContinent = pd.read_csv(path.dirname(__file__) + "/all.csv", usecols=['Country Name', 'region'])

# exemple pour isin pib = pibData[pibData["Country Name"].isin(paysVoulus)]


# PIB / PAYS
print(pibPays)

# POPULATION / PAYS
print(populationPays)

# PIB / CONTINENT
pibContinent = pd.merge(pibPays, paysContinent, on='Country Name')
pibTotalContinent = pibContinent.groupby('region').sum()
print(pibContinent)
print(pibTotalContinent)

# POPULATION / CONTINENT
populationContinent = pd.merge(populationPays, paysContinent, on='Country Name')
populationTotalContinent = populationContinent.groupby('region').sum()
print(populationContinent)
print(populationTotalContinent)

