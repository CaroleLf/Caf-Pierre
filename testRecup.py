import csv
from sqlite3 import Row
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

# source : https://donnees.banquemondiale.org/indicator/EN.ATM.CO2E.KT

paysVoulus = ["France", "Danemark", "Cote d'Ivoire", "China", "India", "United States"]
reader = gpd.read_file("/home/etd/recup/custom.geo.json")


# Evolution empreinte carbone des pays voulu 30 ans 

empreinteCarboneTrente = pd.read_csv("/home/etd/recup/Empreinte_CarboneAPI_EN.ATM.GHGT.KT.CE_DS2_fr_csv_v2_4166498/API_EN.ATM.GHGT.KT.CE_DS2_fr_csv_v2_4166498.csv")
#empreinte = empreinteCarboneTrente[empreinteCarboneTrente["Country Name"].isin(paysVoulus)]
print("Evolution empreinte carbone des pays voulu 30 ans:")
print(empreinteCarboneTrente)



# Empreinte carbone des pays voulu en 2018

empreinteCarbone = pd.read_csv("/home/etd/recup/Empreinte_CarboneAPI_EN.ATM.GHGT.KT.CE_DS2_fr_csv_v2_4166498/API_EN.ATM.GHGT.KT.CE_DS2_fr_csv_v2_4166498.csv", usecols=['Country Name','Indicator Name','2018'])
print("Empreinte carbone des pays voulus :")
print(empreinteCarbone)


# Consommation d'énergie primaire 

consoPrim = pd.read_csv("/home/etd/recup/Conso_Energie_PrimaireAPI_EG.USE.PCAP.KG.OE_DS2_fr_csv_v2_4191987/API_EG.USE.PCAP.KG.OE_DS2_fr_csv_v2_4191987.csv", usecols=['Country Name','Indicator Name','2014'])
print("Consommation d'énergie primaire par pays :")
print(consoPrim)


