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

pibPays = pd.read_csv(path.dirname(__file__) + "/pib.csv")#, usecols=['Country Name', '2020'])
populationPays = pd.read_csv(path.dirname(__file__) + "/pop_totale.csv")#, usecols=['Country Name','2020'])
paysVoulus = ["France", "Denmark", "Cote d'Ivoire", "China", "India", "United States"]
paysContinent = pd.read_csv(path.dirname(__file__) + "/all.csv", usecols=['Country Name', 'region'])

# exemple pour isin pib = pibData[pibData["Country Name"].isin(paysVoulus)]

def calcPIBForAllRegions():
    # PIB / Pays --> CONTINENT
    pibPaysWContinent = pd.merge(pibPays, paysContinent, on='Country Name')
    
    # PIB / CONTINENT
    pibTotalContinent = pibPaysWContinent.groupby('region').sum()
    
    # PIB / Pays + Continents
    pibPaysEtContinents = pd.concat([pibPaysWContinent,pibTotalContinent])
    
    return pibPaysEtContinents

def calcPopulationForAllRegions():
    # POP / Pays --> CONTINENT
    popPaysWContinent = pd.merge(populationPays, paysContinent, on='Country Name')
    
    # POPULATION / CONTINENT
    populationTotalContinent = popPaysWContinent.groupby('region').sum()

    # POP / Pays + Continents
    popPaysEtContinents = pd.concat([popPaysWContinent,populationTotalContinent])
    
    return popPaysEtContinents

print(calcPIBForAllRegions())
print(calcPopulationForAllRegions())