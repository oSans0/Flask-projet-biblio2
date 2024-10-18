from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def home():
    return render_template('hello.html')  # Crée une page d'accueil
 
@app.route('/livres') 
def liste_livres():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)  # Affiche la liste des livres

@app.route('/enregistrer_livre', methods=['GET', 'POST'])
def enregistrer_livre():
    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        genre = request.form['genre']
        date_publication = request.form['date_publication']
        quantite = request.form['quantite']

        # Connexion à la base de données
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Exécution de la requête SQL pour insérer un nouveau livre
        cursor.execute('INSERT INTO Bibliotheque (titre, auteur, genre, date_publication, quantite) VALUES (?, ?, ?, ?, ?)',
                       (titre, auteur, genre, date_publication, quantite))
        conn.commit()
        conn.close()
        return redirect('/livres')  # Redirige vers la liste des livres après l'enregistrement

    return render_template('formulaire_livre.html')  # Affiche le formulaire pour enregistrer un livre

@app.route('/emprunter_livre/<int:id_livre>', methods=['POST'])
def emprunter_livre(id_livre):
    # Ici, tu devras gérer l'emprunt d'un livre
    # Exemple simple : tu peux réduire la quantité du livre emprunté
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE Bibliotheque SET quantite = quantite - 1 WHERE ID_livre = ?', (id_livre,))
    conn.commit()
    conn.close()
    return redirect('/livres')  # Redirige vers la liste des livres

if __name__ == "__main__":
    app.run(debug=True)
