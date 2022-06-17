import sqlite3
from os import path

conn = sqlite3.connect(path.dirname(__file__) + "/CoffeePierre.db")
c = conn.cursor()

c.execute('''DROP TABLE IF EXISTS Région''')
c.execute('''DROP TABLE IF EXISTS Habitants''')
c.execute('''DROP TABLE IF EXISTS PIB''')
c.execute('''DROP TABLE IF EXISTS 'Primary Energies' ''')
c.execute('''DROP TABLE IF EXISTS 'Greenhouse Gas' ''')
c.execute('''DROP TABLE IF EXISTS Activité''')

c.execute('''
          CREATE TABLE "Région"(
    "idRégion" INT NOT NULL,
    "idActivité" INT NULL,
    "nomRégion" NVARCHAR(255) NOT NULL,
    "estPays" INT NOT NULL,
    "idContinent" INT,
    PRIMARY KEY("idRégion","idActivité"),
    FOREIGN KEY("idContinent") REFERENCES "Région"("idRégion"),
    FOREIGN KEY("idActivité") REFERENCES "Activité"("idActivité")
);
          ''')



c.execute('''
CREATE TABLE "Habitants"(
    "année" INT NOT NULL,
    "idRégion" INT NOT NULL,
    "nbHabitant" INT NULL,
    PRIMARY KEY("année","idRégion"),
    FOREIGN KEY("idRégion") REFERENCES "Région"("idRégion")
);
''')


c.execute('''
CREATE TABLE "PIB"(
    "année" INT NOT NULL,
    "idRégion" INT NOT NULL,
    "PIB" DECIMAL(8, 2) NULL,
    PRIMARY KEY("année","idRégion"),
    FOREIGN KEY("idRégion") REFERENCES "Région"("idRégion")
);
''')


c.execute('''
CREATE TABLE "Primary Energies"(
    "année" INT NOT NULL,
    "nomRégion" NVARCHAR(255) NOT NULL,
    "Oil" DECIMAL(8, 2),
    "Coal" DECIMAL(8, 2),
    "Gas" DECIMAL(8, 2),
    "Hydroelectricity" DECIMAL(8, 2),
    "Nuclear" DECIMAL(8, 2),
    "Biomass and Waste" DECIMAL(8, 2),
    "Wind" DECIMAL(8, 2),
    "Fuel Ethanol" DECIMAL(8, 2),
    "Solar, Tide, Wave, Fuel Cell" DECIMAL(8, 2),
    "Geothermal" DECIMAL(8, 2),
    "Biodiesel" DECIMAL(8, 2),
    PRIMARY KEY("année","nomRégion"),
    FOREIGN KEY("nomRégion") REFERENCES "Région"("nomRégion")
    );
''')

c.execute('''
CREATE TABLE "Greenhouse Gas"(
    "année" INT NOT NULL,
    "nomRégion" NVARCHAR(255) NOT NULL,
    "Energy" DECIMAL(8, 2),
    "Agriculture" DECIMAL(8, 2),
    "Industry and Construction" DECIMAL(8, 2),
    "Waste" DECIMAL(8, 2),
    "Other Sectors" DECIMAL(8, 2),
    PRIMARY KEY("année","nomRégion"),
    FOREIGN KEY("nomRégion") REFERENCES "Région"("nomRégion")
);
''')


c.execute('''
CREATE TABLE "Activité"(
    "nomActivité" NVARCHAR(255) NOT NULL,
    "empreinte" INT NOT NULL,
    PRIMARY KEY("nomActivité")
);
''')

conn.commit()