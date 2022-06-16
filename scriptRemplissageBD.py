import sqlite3
from tkinter import S
import pandas as pd
from os import path

empreinteCarbone = pd.read_csv(path.dirname(__file__) + "/testDasha/primary_energy.csv")
empreinteCarbone2018 = pd.read_csv(path.dirname(__file__) + "/testDasha/primary_energy.csv", usecols=['Country Name','Indicator Name','2018'])
pibPays = pd.read_csv(path.dirname(__file__) + "/script-df/pib.csv")
populationPays = pd.read_csv(path.dirname(__file__) + "/script-df/pop_totale.csv")
paysPaysEtContinent = pd.read_csv(path.dirname(__file__) + "/script-df/all.csv", usecols=['Country Name', 'region'])
paysPaysEtContinent['Country Name'] = paysPaysEtContinent['Country Name'].str.replace("ô", "o")

ActPlusCarbone = pd.read_csv(path.dirname(__file__) + "/ActiviteAvecLePlusDempreinteCarbonesur1an.csv")
NBACTIVITE = ActPlusCarbone.shape[1]-1

ghouse_china = pd.read_csv(path.dirname(__file__) + "/testDasha/greenhouse_gas/greenhouse_gas_china.csv", sep=";")
ghouse_coteivoire = pd.read_csv(path.dirname(__file__) + "/testDasha/greenhouse_gas/greenhouse_gas_coteivoire.csv", sep=";")
ghouse_denmark = pd.read_csv(path.dirname(__file__) + "/testDasha/greenhouse_gas/greenhouse_gas_denmark.csv", sep=";")
ghouse_france = pd.read_csv(path.dirname(__file__) + "/testDasha/greenhouse_gas/greenhouse_gas_france.csv", sep=";")
ghouse_inde = pd.read_csv(path.dirname(__file__) + "/testDasha/greenhouse_gas/greenhouse_gas_inde.csv", sep=";")
ghouse_unitedstate = pd.read_csv(path.dirname(__file__) + "/testDasha/greenhouse_gas/greenhouse_gas_unitedstate.csv", sep=";")
ghouse_world = pd.read_csv(path.dirname(__file__) + "/testDasha/greenhouse_gas/greenhouse_gas_world.csv", sep=";")

primary_energy_china = pd.read_csv(path.dirname(__file__) + "/testDasha/primary_energy/primary_energy_china.csv", sep=";")
primary_energy_coteivoire= pd.read_csv(path.dirname(__file__) + "/testDasha/primary_energy/primary_energy_coteivoire.csv", sep=";")
primary_energy_denmark= pd.read_csv(path.dirname(__file__) + "/testDasha/primary_energy/primary_energy_denmark.csv", sep=";")
primary_energy_france= pd.read_csv(path.dirname(__file__) + "/testDasha/primary_energy/primary_energy_france.csv", sep=";")
primary_energy_india= pd.read_csv(path.dirname(__file__) + "/testDasha/primary_energy/primary_energy_india.csv", sep=";")
primary_energy_unitedstates= pd.read_csv(path.dirname(__file__) + "/testDasha/primary_energy/primary_energy_unitedstates.csv", sep=";")
primary_energy_world= pd.read_csv(path.dirname(__file__) + "/testDasha/primary_energy/primary_energy_world.csv", sep=";")
paysVoulus = ["France", "Denmark", "Cote d'Ivoire", "China", "India", "United States"]

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
    conn.commit()

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
    conn.commit()

def fillRegions():
    """
    Fonction de remplissage de la table Région
    """
    df = getRegions()
    df = df.reset_index()
    df['Region Name'] = df['Region Name'].str.replace("""'""", """''""")
    idAct=0
    for idReg, row in df.iterrows():
        if str(row['ContainedBy']) != 'nan':
            for i in range(NBACTIVITE):
                i = df[df['Region Name'] == row['ContainedBy']]
                i = i.values.tolist()[0][0]
                
                c.execute(f'''
                insert into Région (idRégion, nomRégion, estPays,idContinent,idActivité)
                values
                ('{idReg}','{row['Region Name']}','1','{i}','{idAct}')
                ''')
                idAct+=1
        else:
            for i in range(NBACTIVITE):
                c.execute(f'''
                insert into Région (idRégion, nomRégion, estPays,idActivité)
                values
                ('{idReg}','{row['Region Name']}','0','{idAct}')
                ''')
                idAct+=1
    conn.commit()    

def fillActivité():
    for a, row in ActPlusCarbone.iterrows():
        c.execute(f'''
                        insert into Activité (nomActivité, empreinte)
                        values
                        ('{row['Sector']}','{row['Empreinte carbone en MtCO2']}')
                        ''')
        conn.commit()

def fillGreenhouse():
    for a, row in ghouse_china.iterrows():            
        c.execute(f'''
                insert into 'Greenhouse Gas' (année, nomRégion, Energy, Agriculture, 'Industry and Construction', Waste, 'Other Sectors')
                values
                ('{row['Unnamed: 0'][:4]}','China', '{row['Energy']}', '{row['Agriculture']}', '{row['Industry and Construction']}', '{row['Waste']}', '{row['Other Sectors']}')
                ''')
        conn.commit()
    for a, row in ghouse_coteivoire.iterrows():
        c.execute(f'''
                insert into 'Greenhouse Gas' (année, nomRégion, Energy, Agriculture, 'Industry and Construction', Waste, 'Other Sectors')
                values
                ('{row['Unnamed: 0'][:4]}','Cote d''Ivoire', '{row['Energy']}', '{row['Agriculture']}', '{row['Industry and Construction']}', '{row['Waste']}', '{row['Other Sectors']}')
                ''')
        conn.commit()
    for a, row in ghouse_denmark.iterrows():
        c.execute(f'''
                insert into 'Greenhouse Gas' (année, nomRégion, Energy, Agriculture, 'Industry and Construction', Waste, 'Other Sectors')
                values
                ('{row['Unnamed: 0'][:4]}','Denmark', '{row['Energy']}', '{row['Agriculture']}', '{row['Industry and Construction']}', '{row['Waste']}', '{row['Other Sectors']}')
                ''')
        conn.commit()
    for a, row in ghouse_france.iterrows():
        c.execute(f'''
                insert into 'Greenhouse Gas' (année, nomRégion, Energy, Agriculture, 'Industry and Construction', Waste, 'Other Sectors')
                values
                ('{row['Unnamed: 0'][:4]}','France', '{row['Energy']}', '{row['Agriculture']}', '{row['Industry and Construction']}', '{row['Waste']}', '{row['Other Sectors']}')
                ''')
        conn.commit()
    for a, row in ghouse_inde.iterrows():
        c.execute(f'''
                insert into 'Greenhouse Gas' (année, nomRégion, Energy, Agriculture, 'Industry and Construction', Waste, 'Other Sectors')
                values
                ('{row['Unnamed: 0'][:4]}','India', '{row['Energy']}', '{row['Agriculture']}', '{row['Industry and Construction']}', '{row['Waste']}', '{row['Other Sectors']}')
                ''')
        conn.commit()
    for a, row in ghouse_unitedstate.iterrows():
        c.execute(f'''
                insert into 'Greenhouse Gas' (année, nomRégion, Energy, Agriculture, 'Industry and Construction', Waste, 'Other Sectors')
                values
                ('{row['Unnamed: 0'][:4]}','United States', '{row['Energy']}', '{row['Agriculture']}', '{row['Industry and Construction']}', '{row['Waste']}', '{row['Other Sectors']}')
                ''')
        conn.commit()

"""
def fillEmpreinteCarbone():
    '''
    Fonction de remplissage de la table Empreinte_Carbone
    ''''''
    df = empreinteCarbone
    df['Country Name'] = df['Country Name'].str.replace("'", "''")
    regions = df.values

    for col_name, col in df.transpose().iterrows():
        dates = [str(year) for year in range(1959,2022)]
        if col_name in dates:
            i = 0
            
            for val in col.values:
                c.execute(f'''SELECT idRégion FROM Région WHERE nomRégion = '{regions[i][0]}' ''')
                id = c.fetchone()
                print(id)
                if val == float('nan'):
                    c.execute(f'''
                        insert into Empreinte_Carbone ('année', 'idRégion')
                        values
                        ('{col_name}','{id[0]}')
                        ''')
                elif str(id) == "None":
                    pass
                else:
                    c.execute(f'''
                        insert into Empreinte_Carbone ('année', 'idRégion', 'produit')
                        values
                        ('{col_name}','{id[0]}','{val}')
                        ''')
                i+=1
    conn.commit()
"""
fillPIB()
fillHabitants()
fillRegions()
fillActivité()
fillGreenhouse()
#fillEmpreinteCarbone()

conn.commit()

"""
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
"""