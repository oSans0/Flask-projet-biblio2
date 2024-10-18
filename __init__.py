from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def home():
    return render_template('login.html')  # Crée une page d'accueil
  
@app.route('/livres') 
def liste_livres():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Bibliotheque;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)  # Affiche la liste des livres

@app.route('/Users') 
def Users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Utilisateur;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data2.html', data=data)  # Affiche la liste des livres

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

@app.route('/fiche_livre/<string:nom_livre>')
def ReadLivre(nom_livre):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Bibliotheque WHERE titre = ?', (nom_livre,))
    data = cursor.fetchall()
    conn.close()
    
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/emprunter_livre', methods=['GET', 'POST'])
def emprunter_livre():
    if request.method == 'POST':
        # Récupérer l'ID du livre sélectionné dans le formulaire
        id_livre = request.form['id_livre']
        
        # Connexion à la base de données et mise à jour
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE Bibliotheque SET quantite = quantite - 1 WHERE ID_livre = ?', (id_livre,))
        conn.commit()
        conn.close()

        return redirect('/livres')  # Redirige vers la liste des livres après l'emprunt

    # Si c'est une requête GET, on affiche la liste des livres pour l'emprunt
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT ID_livre, titre FROM Bibliotheque WHERE quantite > 0')
    livres = cursor.fetchall()  # Récupérer les livres disponibles pour l'emprunt
    conn.close()

    return render_template('emprunter_livre.html', livres=livres)

@app.route('/supprimer_livre/<int:id_livre>', methods=['POST'])
def supprimer_livre(id_livre):
    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Exécuter la requête pour supprimer un livre
    cursor.execute('DELETE FROM Bibliotheque WHERE ID_livre = ?', (id_livre,))
    conn.commit()
    conn.close()

    # Rediriger vers la liste des livres après la suppression
    return redirect('/livres')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('INSERT INTO Users (username, password) VALUES (?, ?)',(username, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user['id']
            return redirect(url_for('livres'))
        else:
            return "Identifiants incorrects"

    return render_template('login.html')

# Route pour la déconnexion
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
