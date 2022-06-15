import sqlite3
from tkinter import S
import pandas as pd
from os import path

empreinteCarboneTrenteAnnee = pd.read_csv(path.dirname(__file__) + "/Empreinte_CarboneAPI_EN.ATM.GHGT.KT.CE_DS2_fr_csv_v2_4166498/API_EN.ATM.GHGT.KT.CE_DS2_fr_csv_v2_4166498.csv")
empreinteCarbone2018 = pd.read_csv(path.dirname(__file__) + "/Empreinte_CarboneAPI_EN.ATM.GHGT.KT.CE_DS2_fr_csv_v2_4166498/API_EN.ATM.GHGT.KT.CE_DS2_fr_csv_v2_4166498.csv", usecols=['Country Name','Indicator Name','2018'])
pibPays = pd.read_csv(path.dirname(__file__) + "/script-df/pib.csv")
populationPays = pd.read_csv(path.dirname(__file__) + "/script-df/pop_totale.csv")
paysPaysEtContinent = pd.read_csv(path.dirname(__file__) + "/script-df/all.csv", usecols=['Country Name', 'region'])
#NiveauMer = pd.read_csv(path.dirname(__file__) + "/CMIP6 - Sea level rise (SLR) Change meters - Long Term (2081-2100) SSP5-8.5 (rel. to 1995-2014) - Annual .csv")

paysVoulus = ["France", "Denmark", "Cote d'Ivoire", "China", "India", "United States"]
activités = ["Industrie","Transport","Residentiel","Commerce et services publiques","Agriculture","Autres"]

conn = sqlite3.connect(path.dirname(__file__) + "/CoffeePierre.db")
c = conn.cursor()

# exemple pour isin pib = pibData[pibData["Country Name"].isin(paysVoulus)]

def calcPIBForAllRegions():
    # PIB / Pays --> CONTINENT
    pibPaysWContinent = pd.merge(pibPays, paysPaysEtContinent, on='Country Name')
    
    # PIB / CONTINENT
    pibTotalContinent = pibPaysWContinent.groupby('region').sum()
    
    # PIB / Pays + Continents
    pibPaysEtContinents = pd.concat([pibPaysWContinent,pibTotalContinent])
    
    return pibPaysEtContinents

def calcPopulationForAllRegions():
    # POP / Pays --> CONTINENT
    popPaysWContinent = pd.merge(populationPays, paysPaysEtContinent, on='Country Name')
    
    # POPULATION / CONTINENT
    populationTotalContinent = popPaysWContinent.groupby('region').sum()

    # POP / Pays + Continents
    popPaysEtContinents = pd.concat([popPaysWContinent,populationTotalContinent])
    
    return popPaysEtContinents

def getRegions():
    df = calcPopulationForAllRegions()
    df = df[['Country Name','region']]
    df.rename(columns={'Country Name':'Region Name', 'region':'ContainedBy'}, inplace = True)
    for id in df.index:
        if not str(id).isnumeric():
            df.at[id,'Region Name'] = id
    df.set_index(pd.Index([i for i in range(len(df.index))]), inplace = True)
    return df

def fillPIB():
    """
    Fonction de remplissage de la table PIB
    """
    df = calcPIBForAllRegions()
    df = df.reset_index()
    
    for col_name, col in df.transpose().iterrows():
        dates = [str(year) for year in range(1959,2022)]
        if col_name in dates:
            i = 0
            for val in col.values:
                if val == float('nan'):
                    c.execute(f'''
                        insert into PIB ('année', 'idRégion')
                        values
                        ('{col_name}','{i}')
                        ''')
                else:
                    c.execute(f'''
                        insert into PIB ('année', 'idRégion', 'PIB')
                        values
                        ('{col_name}','{i}','{val}')
                        ''')
                i+=1

def fillHabitants():
    """
    Fonction de remplissage de la table Habitants
    """
    df = calcPopulationForAllRegions()
    df = df.reset_index()
    
    for col_name, col in df.transpose().iterrows():
        dates = [str(year) for year in range(1959,2022)]
        if col_name in dates:
            i = 0
            for val in col.values:
                if val == float('nan'):
                    c.execute(f'''
                        insert into Habitants ('année', 'idRégion')
                        values
                        ('{col_name}','{i}')
                        ''')
                else:
                    c.execute(f'''
                        insert into Habitants ('année', 'idRégion', 'nbHabitant')
                        values
                        ('{col_name}','{i}','{val}')
                        ''')
                i+=1

def fillRegions():
    """
    Fonction de remplissage de la table Région
    """
    df = getRegions()
    df = df.reset_index()
    df['Region Name'] = df['Region Name'].str.replace("""'""", """''""")
    for idReg, row in df.iterrows():
        idAct=0
        if str(row['ContainedBy']) != 'nan':
            for i in range(len(activités)):
                i = df[df['Region Name'] == row['ContainedBy']]
                i = i.values.tolist()[0][0]
                
                c.execute(f'''
                insert into Région (idRégion, nomRégion, estPays,idContinent,idActivité)
                values
                ('{idReg}','{row['Region Name']}','1','{i}','{idAct}')
                ''')
                idAct+=1
        else:
            for i in range(len(activités)):
                c.execute(f'''
                insert into Région (idRégion, nomRégion, estPays,idActivité)
                values
                ('{idReg}','{row['Region Name']}','0','{idAct}')
                ''')
                idAct+=1
    conn.commit()    

def fillActivité():
    secteursActivités = ["Industrie","Transport","Residentiel","Commerce et service publique","Agriculture"]
    for i in range(len(secteursActivités)):
        c.execute(f'''
            insert into Activité ('idActivité', 'nomActivité')
            values
            ('{i}','{secteursActivités[i]}')
            ''')

fillPIB()
fillHabitants()
#fillActivité()
fillRegions()

conn.commit()

"""
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

"""

c.execute('''SELECT * FROM Activité''')
df = pd.DataFrame(c.fetchall())
print(df)