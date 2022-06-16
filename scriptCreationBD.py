import sqlite3
from os import path

conn = sqlite3.connect(path.dirname(__file__) + "/CoffeePierre.db")
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
CREATE TABLE "Empreinte_Carbone"(
    "année" INT NOT NULL,
    "idRégion" INT NOT NULL,
    "produit" DECIMAL(8, 2) NULL,
    PRIMARY KEY("année","idRégion"),
    FOREIGN KEY("idRégion") REFERENCES "Région"("idRégion")
    );
''')


c.execute('''
CREATE TABLE "Activité"(
    "nomActivité" NVARCHAR(255) NOT NULL,
    "empreinte" INT NOT NULL,
    PRIMARY KEY("nomActivité")
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