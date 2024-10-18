import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO Bibliotheque (titre, auteur, genre, date_publication, quantite) VALUES (?, ?, ?, ?, ?)",('Les Misérables', 'Victor Hugo', 'Roman', '1862-01-01', 5))
cur.execute("INSERT INTO Bibliotheque (titre, auteur, genre, date_publication, quantite) VALUES (?, ?, ?, ?, ?)",('Le Petit Prince', 'Antoine de Saint-Exupéry', 'Fable', '1943-04-06', 10))
cur.execute("INSERT INTO Bibliotheque (titre, auteur, genre, date_publication, quantite) VALUES (?, ?, ?, ?, ?)",('1984', 'George Orwell', 'Dystopie', '1949-06-08', 7))
cur.execute("INSERT INTO Bibliotheque (titre, auteur, genre, date_publication, quantite) VALUES (?, ?, ?, ?, ?)",('Moby Dick', 'Herman Melville', 'Aventure', '1851-10-18', 3))
cur.execute("INSERT INTO Bibliotheque (titre, auteur, genre, date_publication, quantite) VALUES (?, ?, ?, ?, ?)",('L\'Étranger', 'Albert Camus', 'Roman', '1942-05-19', 6))
cur.execute("INSERT INTO Bibliotheque (titre, auteur, genre, date_publication, quantite) VALUES (?, ?, ?, ?, ?)",('Don Quichotte', 'Miguel de Cervantes', 'Aventure', '1605-01-16', 4))
cur.execute("INSERT INTO Bibliotheque (titre, auteur, genre, date_publication, quantite) VALUES (?, ?, ?, ?, ?)",('La Divine Comédie', 'Dante Alighieri', 'Épopée', '1320-01-01', 2))
cur.execute("INSERT INTO Bibliotheque (titre, auteur, genre, date_publication, quantite) VALUES (?, ?, ?, ?, ?)",('Le Seigneur des Anneaux', 'J.R.R. Tolkien', 'Fantasy', '1954-07-29', 8))

connection.commit()
connection.close()
