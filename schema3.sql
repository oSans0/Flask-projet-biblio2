CREATE TABLE IF NOT EXISTS Emprunts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    livre_id INTEGER NOT NULL,
    date_emprunt DATE DEFAULT CURRENT_DATE,
    date_retour DATE,
    FOREIGN KEY(user_id) REFERENCES Utilisateur(id),
    FOREIGN KEY(livre_id) REFERENCES Bibliotheque(ID_livre)
);
