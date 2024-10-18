import sqlite3

connection = sqlite3.connect('database.db')

with open('schema3.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO Utilisateur (username, password) VALUES (?, ?)",('YUI', 12345))
cur.execute("INSERT INTO Utilisateur (username, password) VALUES (?, ?)",('LEROUX', 12345))
cur.execute("INSERT INTO Utilisateur (username, password) VALUES (?, ?)",('MARTIN', 12345))

connection.commit()
connection.close()
