import sqlite3
import pandas as pd
from os import path

pibPays = pd.read_csv(path.dirname(__file__) + "/application/csv/pib.csv")
populationPays = pd.read_csv(path.dirname(__file__) + "/application/csv/pop_totale.csv")
paysPaysEtContinent = pd.read_csv(path.dirname(__file__) + "/application/csv/all.csv", usecols=['Country Name', 'region'])
paysPaysEtContinent['Country Name'] = paysPaysEtContinent['Country Name'].str.replace("ô", "o")

ActPlusCarbone = pd.read_csv(path.dirname(__file__) + "/ActiviteAvecLePlusDempreinteCarbonesur1an.csv")
NBACTIVITE = ActPlusCarbone.shape[1]-1

ghouse_china = pd.read_csv(path.dirname(__file__) + "/application/greenhouse_gas/greenhouse_gas_china.csv", sep=";")
ghouse_coteivoire = pd.read_csv(path.dirname(__file__) + "/application/greenhouse_gas/greenhouse_gas_coteivoire.csv", sep=";")
ghouse_denmark = pd.read_csv(path.dirname(__file__) + "/application/greenhouse_gas/greenhouse_gas_denmark.csv", sep=";")
ghouse_france = pd.read_csv(path.dirname(__file__) + "/application/greenhouse_gas/greenhouse_gas_france.csv", sep=";")
ghouse_inde = pd.read_csv(path.dirname(__file__) + "/application/greenhouse_gas/greenhouse_gas_inde.csv", sep=";")
ghouse_unitedstate = pd.read_csv(path.dirname(__file__) + "/application/greenhouse_gas/greenhouse_gas_unitedstate.csv", sep=";")
ghouse_germany = pd.read_csv(path.dirname(__file__) + "/application/greenhouse_gas/greenhouse_gas_germany.csv", sep=";")

primary_energy_china = pd.read_csv(path.dirname(__file__) + "/application/primary_energy/primary_energy_china.csv", sep=";")
primary_energy_coteivoire= pd.read_csv(path.dirname(__file__) + "/application/primary_energy/primary_energy_coteivoire.csv", sep=";")
primary_energy_denmark= pd.read_csv(path.dirname(__file__) + "/application/primary_energy/primary_energy_denmark.csv", sep=";")
primary_energy_france= pd.read_csv(path.dirname(__file__) + "/application/primary_energy/primary_energy_france.csv", sep=";")
primary_energy_india= pd.read_csv(path.dirname(__file__) + "/application/primary_energy/primary_energy_india.csv", sep=";")
primary_energy_unitedstates= pd.read_csv(path.dirname(__file__) + "/application/primary_energy/primary_energy_unitedstates.csv", sep=";")
primary_energy_germany= pd.read_csv(path.dirname(__file__) + "/application/primary_energy/primary_energy_germany.csv", sep=";")

conn = sqlite3.connect(path.dirname(__file__) + "/CoffeePierre.db")
c = conn.cursor()

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
    c.execute(f'''
                        insert into Habitants ('année', 'idRégion', 'nbHabitant')
                        values
                        ('2020','999','7763498647')
                        ''')
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
    c.execute(f'''
                insert into Région (idRégion, nomRégion, estPays)
                values
                ('999','World','0')
                ''')
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
    #Pas très beau, mais c'était le plus rapide à faire
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
    for a, row in ghouse_germany.iterrows():
        c.execute(f'''
                insert into 'Greenhouse Gas' (année, nomRégion, Energy, Agriculture, 'Industry and Construction', Waste, 'Other Sectors')
                values
                ('{row['Unnamed: 0'][:4]}','Germany', '{row['Energy']}', '{row['Agriculture']}', '{row['Industry and Construction']}', '{row['Waste']}', '{row['Other Sectors']}')
                ''')
        conn.commit()

def fillPrimaryEnergy():
    for a, row in primary_energy_china.iterrows():
        c.execute(f'''
                insert into 'Primary Energies' (année, nomRégion, Oil, Coal, Gas, Hydroelectricity, Nuclear, 'Biomass and Waste',Wind,'Fuel Ethanol','Solar, Tide, Wave, Fuel Cell',Geothermal,Biodiesel)
                values
                ('{row['Unnamed: 0'][:4]}','China','{row['Oil']}','{row['Coal']}','{row['Gas']}','{row['Hydroelectricity']}','{row['Nuclear']}','{row['Biomass and Waste']}','{row['Wind']}','{row['Fuel Ethanol']}','{row['Solar, Tide, Wave, Fuel Cell']}','{row['Geothermal']}','{row['Biodiesel']}')
        ''')
    for a, row in primary_energy_coteivoire.iterrows():
        c.execute(f'''
                insert into 'Primary Energies' (année, nomRégion, Oil, Coal, Gas, Hydroelectricity, Nuclear, 'Biomass and Waste',Wind,'Fuel Ethanol','Solar, Tide, Wave, Fuel Cell',Geothermal,Biodiesel)
                values
                ('{row['Unnamed: 0'][:4]}','Cote d''Ivoire','{row['Oil']}','{row['Coal']}','{row['Gas']}','{row['Hydroelectricity']}','{row['Nuclear']}','{row['Biomass and Waste']}','{row['Wind']}','{row['Fuel Ethanol']}','{row['Solar, Tide, Wave, Fuel Cell']}','{row['Geothermal']}','{row['Biodiesel']}')
        ''')
    for a, row in primary_energy_denmark.iterrows():
        c.execute(f'''
                insert into 'Primary Energies' (année, nomRégion, Oil, Coal, Gas, Hydroelectricity, Nuclear, 'Biomass and Waste',Wind,'Fuel Ethanol','Solar, Tide, Wave, Fuel Cell',Geothermal,Biodiesel)
                values
                ('{row['Unnamed: 0'][:4]}','Denmark','{row['Oil']}','{row['Coal']}','{row['Gas']}','{row['Hydroelectricity']}','{row['Nuclear']}','{row['Biomass and Waste']}','{row['Wind']}','{row['Fuel Ethanol']}','{row['Solar, Tide, Wave, Fuel Cell']}','{row['Geothermal']}','{row['Biodiesel']}')
        ''')
    for a, row in primary_energy_france.iterrows():
        c.execute(f'''
                insert into 'Primary Energies' (année, nomRégion, Oil, Coal, Gas, Hydroelectricity, Nuclear, 'Biomass and Waste',Wind,'Fuel Ethanol','Solar, Tide, Wave, Fuel Cell',Geothermal,Biodiesel)
                values
                ('{row['Unnamed: 0'][:4]}','France','{row['Oil']}','{row['Coal']}','{row['Gas']}','{row['Hydroelectricity']}','{row['Nuclear']}','{row['Biomass and Waste']}','{row['Wind']}','{row['Fuel Ethanol']}','{row['Solar, Tide, Wave, Fuel Cell']}','{row['Geothermal']}','{row['Biodiesel']}')
        ''')
    for a, row in primary_energy_india.iterrows():
        c.execute(f'''
                insert into 'Primary Energies' (année, nomRégion, Oil, Coal, Gas, Hydroelectricity, Nuclear, 'Biomass and Waste',Wind,'Fuel Ethanol','Solar, Tide, Wave, Fuel Cell',Geothermal,Biodiesel)
                values
                ('{row['Unnamed: 0'][:4]}','India','{row['Oil']}','{row['Coal']}','{row['Gas']}','{row['Hydroelectricity']}','{row['Nuclear']}','{row['Biomass and Waste']}','{row['Wind']}','{row['Fuel Ethanol']}','{row['Solar, Tide, Wave, Fuel Cell']}','{row['Geothermal']}','{row['Biodiesel']}')
        ''')
    for a, row in primary_energy_unitedstates.iterrows():
        c.execute(f'''
                insert into 'Primary Energies' (année, nomRégion, Oil, Coal, Gas, Hydroelectricity, Nuclear, 'Biomass and Waste',Wind,'Fuel Ethanol','Solar, Tide, Wave, Fuel Cell',Geothermal,Biodiesel)
                values
                ('{row['Unnamed: 0'][:4]}','United States','{row['Oil']}','{row['Coal']}','{row['Gas']}','{row['Hydroelectricity']}','{row['Nuclear']}','{row['Biomass and Waste']}','{row['Wind']}','{row['Fuel Ethanol']}','{row['Solar, Tide, Wave, Fuel Cell']}','{row['Geothermal']}','{row['Biodiesel']}')
        ''')
    for a, row in primary_energy_germany.iterrows():
        c.execute(f'''
                insert into 'Primary Energies' (année, nomRégion, Oil, Coal, Gas, Hydroelectricity, Nuclear, 'Biomass and Waste',Wind,'Fuel Ethanol','Solar, Tide, Wave, Fuel Cell',Geothermal,Biodiesel)
                values
                ('{row['Unnamed: 0'][:4]}','Germany','{row['Oil']}','{row['Coal']}','{row['Gas']}','{row['Hydroelectricity']}','{row['Nuclear']}','{row['Biomass and Waste']}','{row['Wind']}','{row['Fuel Ethanol']}','{row['Solar, Tide, Wave, Fuel Cell']}','{row['Geothermal']}','{row['Biodiesel']}')
        ''')

fillPIB()
fillHabitants()
fillRegions()
fillActivité()
fillGreenhouse()
fillPrimaryEnergy()

conn.commit()