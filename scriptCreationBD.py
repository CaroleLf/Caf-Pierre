import sqlite3

conn = sqlite3.connect("./sae_s204-s205/SAE2.04_2.05/CoffeePierre.db")
c = conn.cursor()

c.execute('''DROP TABLE IF EXISTS Région''')
c.execute('''DROP TABLE IF EXISTS Habitants''')
c.execute('''DROP TABLE IF EXISTS PIB''')
c.execute('''DROP TABLE IF EXISTS Empreinte_Carbone''')
c.execute('''DROP TABLE IF EXISTS Activité''')
c.execute('''DROP TABLE IF EXISTS Energie''')
c.execute('''DROP TABLE IF EXISTS Effets''')

c.execute('''
          CREATE TABLE "Région"(
    "idRégion" INT NOT NULL,
    "nomRégion" NVARCHAR(255) NOT NULL,
    "estPays" INT NOT NULL,
    "idContinent" INT NULL,
    "idActivité" INT NULL,
    PRIMARY KEY("idRégion"),
    FOREIGN KEY("idContinent") REFERENCES "Région"("idRégion"),
    FOREIGN KEY("idActivité") REFERENCES "Activité"("idActivité")
);
          ''')



c.execute('''
CREATE TABLE "Habitants"(
    "année" INT NOT NULL,
    "idRégion" INT NOT NULL,
    "nbHabitant" INT NOT NULL,
    PRIMARY KEY("année","idRégion"),
    FOREIGN KEY("idRégion") REFERENCES "Région"("idRégion")
);
''')


c.execute('''
CREATE TABLE "PIB"(
    "année" INT NOT NULL,
    "idRégion" INT NOT NULL,
    "PIB" DECIMAL(8, 2) NOT NULL,
    PRIMARY KEY("année","idRégion"),
    FOREIGN KEY("idRégion") REFERENCES "Région"("idRégion")
);
''')


c.execute('''
CREATE TABLE "Empreinte_Carbone"(
    "année" INT NOT NULL,
    "idActivité" INT NOT NULL,
    "produit" DECIMAL(8, 2) NOT NULL,
    PRIMARY KEY("année","idActivité"),
    FOREIGN KEY("idActivité") REFERENCES "Activité"("idActivité")
);
''')


c.execute('''
CREATE TABLE "Activité"(
    "idActivité" INT NOT NULL,
    "nomActivité" NVARCHAR(255) NOT NULL,
    PRIMARY KEY("idActivité")
);
''')


c.execute('''
CREATE TABLE "Energie"(
    "idEnergies" INT NOT NULL,
    "année" INT NOT NULL,
    "idActivité" INT NOT NULL,
    "nomEnergie" NVARCHAR(255) NOT NULL,
    "estPrimaire" INT NOT NULL,
    "consommation" DECIMAL(8, 2) NOT NULL,
    PRIMARY KEY("idEnergies","année","idActivité"),
    FOREIGN KEY("idActivité") REFERENCES "Activité"("idActivité")
);
''')


c.execute('''
CREATE TABLE "Effets"(
    "année" INT NOT NULL,
    "idRégion" INT NOT NULL,
    "changementTempérature" FLOAT NOT NULL,
    "montéeEaux" FLOAT NOT NULL,
    PRIMARY KEY("année","idRégion"),
    FOREIGN KEY("idRégion") REFERENCES "Région"("idRégion")
);
''')

conn.commit()