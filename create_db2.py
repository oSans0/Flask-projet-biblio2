import sqlite3

connection = sqlite3.connect('database.db')

with open('schema2.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO clients (nom, prenom) VALUES (?, ?)",('DUPONT', 'Emilie'))
cur.execute("INSERT INTO clients (nom, prenom) VALUES (?, ?)",('LEROUX', 'Lucas'))
cur.execute("INSERT INTO clients (nom, prenom) VALUES (?, ?)",('MARTIN', 'Amandine'))
cur.execute("INSERT INTO clients (nom, prenom) VALUES (?, ?)",('TREMBLAY', 'Antoine'))
cur.execute("INSERT INTO clients (nom, prenom) VALUES (?, ?)",('LAMBERT', 'Sarah'))
cur.execute("INSERT INTO clients (nom, prenom) VALUES (?, ?)",('GAGNON', 'Nicolas'))
cur.execute("INSERT INTO clients (nom, prenom) VALUES (?, ?)",('DUBOIS', 'Charlotte'))
cur.execute("INSERT INTO clients (nom, prenom) VALUES (?, ?)",('LEFEVRE', 'Thomas'))

connection.commit()
connection.close()
