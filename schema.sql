DROP TABLE IF EXISTS Bibliotheque;

CREATE TABLE Bibliotheque (
    ID_livre INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    auteur TEXT NOT NULL,
    genre TEXT,
    date_publication DATE,
    quantite INTEGER NOT NULL, 
);
