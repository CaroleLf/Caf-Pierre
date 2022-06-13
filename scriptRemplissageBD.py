import sqlite3
import pandas as pd

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


conn.commit()

c.execute('''SELECT * FROM Activité''')
df = pd.DataFrame(c.fetchall())
print(df)