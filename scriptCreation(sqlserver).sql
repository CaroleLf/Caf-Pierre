CREATE TABLE "Région"(
    "idRégion" INT NOT NULL,
    "nomRégion" NVARCHAR(255) NOT NULL,
    "estPays" INT NOT NULL,
    "idContinent" INT NULL,
    "idActivité" INT NULL
);
ALTER TABLE
    "Région" ADD CONSTRAINT "région_idrégion_primary" PRIMARY KEY("idRégion");
ALTER TABLE
    "Région" ADD CONSTRAINT "région_idcontinent_foreign" FOREIGN KEY("idContinent") REFERENCES "Région"("idRégion");
ALTER TABLE
    "Région" ADD CONSTRAINT "région_idactivité_foreign" FOREIGN KEY("idActivité") REFERENCES "Activité"("idActivité");



CREATE TABLE "Habitants"(
    "date" DATE NOT NULL,
    "idRégion" INT NOT NULL,
    "nbHabitant" INT NOT NULL
);
ALTER TABLE
    "Habitants" ADD CONSTRAINT "habitants_date_primary" PRIMARY KEY("date");
ALTER TABLE
    "Habitants" ADD CONSTRAINT "habitants_idrégion_primary" PRIMARY KEY("idRégion");
ALTER TABLE
    "Habitants" ADD CONSTRAINT "habitants_idrégion_foreign" FOREIGN KEY("idRégion") REFERENCES "Région"("idRégion");



CREATE TABLE "PIB"(
    "date" DATE NOT NULL,
    "idRégion" INT NOT NULL,
    "PIB" DECIMAL(8, 2) NOT NULL
);
ALTER TABLE
    "PIB" ADD CONSTRAINT "pib_date_primary" PRIMARY KEY("date");
ALTER TABLE
    "PIB" ADD CONSTRAINT "pib_idrégion_primary" PRIMARY KEY("idRégion");
ALTER TABLE
    "PIB" ADD CONSTRAINT "pib_idrégion_foreign" FOREIGN KEY("idRégion") REFERENCES "Région"("idRégion");


CREATE TABLE "Empreinte_Carbone"(
    "date" DATE NOT NULL,
    "idActivité" INT NOT NULL,
    "produit" DECIMAL(8, 2) NOT NULL
);
ALTER TABLE
    "Empreinte_Carbone" ADD CONSTRAINT "empreinte_carbone_date_primary" PRIMARY KEY("date");
ALTER TABLE
    "Empreinte_Carbone" ADD CONSTRAINT "empreinte_carbone_idactivité_primary" PRIMARY KEY("idActivité");
ALTER TABLE
    "Empreinte_Carbone" ADD CONSTRAINT "empreinte_carbone_idactivité_foreign" FOREIGN KEY("idActivité") REFERENCES "Activité"("idActivité");



CREATE TABLE "Activité"(
    "idActivité" INT NOT NULL,
    "nomActivité" INT NOT NULL
);
ALTER TABLE
    "Activité" ADD CONSTRAINT "activité_idactivité_primary" PRIMARY KEY("idActivité");



CREATE TABLE "Energie"(
    "idEnergies" INT NOT NULL,
    "date" DATE NOT NULL,
    "idActivité" INT NOT NULL,
    "nomEnergie" NVARCHAR(255) NOT NULL,
    "estPrimaire" INT NOT NULL,
    "consommation" DECIMAL(8, 2) NOT NULL
);
ALTER TABLE
    "Energie" ADD CONSTRAINT "energie_idenergies_primary" PRIMARY KEY("idEnergies");
ALTER TABLE
    "Energie" ADD CONSTRAINT "energie_date_primary" PRIMARY KEY("date");
ALTER TABLE
    "Energie" ADD CONSTRAINT "energie_idactivité_primary" PRIMARY KEY("idActivité");
ALTER TABLE
    "Energie" ADD CONSTRAINT "energie_idactivité_foreign" FOREIGN KEY("idActivité") REFERENCES "Activité"("idActivité");



CREATE TABLE "Effets"(
    "date" DATE NOT NULL,
    "idRégion" INT NOT NULL,
    "changementTempérature" FLOAT NOT NULL,
    "montéeEaux" FLOAT NOT NULL
);
ALTER TABLE
    "Effets" ADD CONSTRAINT "effets_date_primary" PRIMARY KEY("date");
ALTER TABLE
    "Effets" ADD CONSTRAINT "effets_idrégion_primary" PRIMARY KEY("idRégion");
ALTER TABLE
    "Effets" ADD CONSTRAINT "effets_idrégion_foreign" FOREIGN KEY("idRégion") REFERENCES "Région"("idRégion");




/////////////
CREATE TABLE produitComment (
    numEnergie int,
    numActivité int,
    PRIMARY KEY(numEnergie,numActivité),
    FOREIGN KEY (numActivité) REFERENCES Activité(NumActivité),
    FOREIGN KEY (numEnergie) REFERENCES TypeEnergie(numEnergie))