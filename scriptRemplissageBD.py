import sqlite3
import pandas as pd
from os import path

empreinteCarboneTrenteAnnee = pd.read_csv(path.dirname(__file__) + "/Empreinte_CarboneAPI_EN.ATM.GHGT.KT.CE_DS2_fr_csv_v2_4166498/API_EN.ATM.GHGT.KT.CE_DS2_fr_csv_v2_4166498.csv")
empreinteCarbone2018 = pd.read_csv(path.dirname(__file__) + "/Empreinte_CarboneAPI_EN.ATM.GHGT.KT.CE_DS2_fr_csv_v2_4166498/API_EN.ATM.GHGT.KT.CE_DS2_fr_csv_v2_4166498.csv", usecols=['Country Name','Indicator Name','2018'])
pibPays = pd.read_csv(path.dirname(__file__) + "/script-df/pib.csv", usecols=['Country Name', '2020'])
populationPays = pd.read_csv(path.dirname(__file__) + "/script-df/pop_totale.csv", usecols=['Country Name','2020'])
paysContinent = pd.read_csv(path.dirname(__file__) + "/script-df/all.csv", usecols=['Country Name', 'region'])
NiveauMer = pd.read_csv(path.dirname(__file__) + "/CMIP6 - Sea level rise (SLR) Change meters - Long Term (2081-2100) SSP5-8.5 (rel. to 1995-2014) - Annual .csv")


paysVoulus = ["France", "Denmark", "Cote d'Ivoire", "China", "India", "United States"]
secteursActivités = ["Industrie","Transport","Residentiel","Commercial",]

conn = sqlite3.connect("./sae_s204-s205/SAE2.04_2.05/CoffeePierre.db")
c = conn.cursor()

for i in range(10):
    c.execute(f'''
    INSERT INTO Activité (idActivité,nomActivité)
        VALUES
        ({i}, '{"act" + str(i)}')
    ''')

for y in range(1970,2022):
    for a in range(10):
        c.execute(f'''
        INSERT INTO Empreinte_Carbone (année,idActivité,produit)
            VALUES
            ({y}, {a}, 8.1)
        ''')

c.execute(f'''
insert into Habitants (année, idRégion, nbHabitant)
    values
    ({"PLACEHOLDER"},{"PLACEHOLDER"},{"PLACEHOLDER"})
''')

for annee in range(1959,2020):
    c.execute(f'''
    insert into PIB ({annee}, idRégion, PIB)
        values
        ({"PLACEHOLDER"},{"PLACEHOLDER"},{"PLACEHOLDER"})
    ''')

c.execute(f'''
insert into Energie (idEnergies, année, idactivité, nomEnergie, estPrimaire, consommation)
    values
    ({"PLACEHOLDER"},{"PLACEHOLDER"},{"PLACEHOLDER"},{"PLACEHOLDER"},{"PLACEHOLDER"},{"PLACEHOLDER"})
''')

c.execute(f'''
insert into Effets (année, idRégion, changementTempérature, montéeEaux)
    values
    ({"PLACEHOLDER"},{"PLACEHOLDER"},{"PLACEHOLDER"},{"PLACEHOLDER"})
''')

c.execute(f'''
insert into Région (idRégion, nomRégion, estPays, idContinent, idActivité)
    values
    ({"PLACEHOLDER"},{"PLACEHOLDER"},{"PLACEHOLDER"},{"PLACEHOLDER"})
''')
conn.commit()

c.execute('''SELECT * FROM Activité''')
df = pd.DataFrame(c.fetchall())
print(df)