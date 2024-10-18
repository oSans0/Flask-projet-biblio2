from flask import Flask, render_template, request, redirect, url_for, session
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

        cursor.execute('INSERT INTO Utilisateur (username, password) VALUES (?, ?)',(username, password))
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
        cursor.execute('SELECT * FROM Utilisateur WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user['id']
            return redirect(url_for('liste_livres'))
        else:
            return "Identifiants incorrects"

    return render_template('login.html')

# Route pour la déconnexion
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/emprunter_livre/<int:id_livre>')
def emprunter_livre(id_livre):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    
    # Connexion à la base de données avec timeout
    conn = sqlite3.connect('database.db', timeout=5)  
    cursor = conn.cursor()

    try:
        # Vérifier si le livre est disponible
        cursor.execute('SELECT quantite FROM Bibliotheque WHERE ID_livre = ?', (id_livre,))
        livre = cursor.fetchone()

        if livre and livre[0] > 0:  # Vérifie la quantité du livre
            # Réduire la quantité et enregistrer l'emprunt
            cursor.execute('UPDATE Bibliotheque SET quantite = quantite - 1 WHERE ID_livre = ?', (id_livre,))
            cursor.execute('INSERT INTO Emprunts (user_id, livre_id) VALUES (?, ?)', (user_id, id_livre))
            conn.commit()
        else:
            # Gérer le cas où le livre n'est pas disponible (facultatif)
            print("Le livre n'est pas disponible.")
    except sqlite3.Error as e:
        print(f"Erreur lors de l'emprunt du livre : {e}")
    finally:
        conn.close()  # S'assurer que la connexion est fermée

    return redirect('/livres')

@app.route('/mes_emprunts')
def mes_emprunts():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    # Récupérer les livres empruntés par l'utilisateur
    cursor.execute('''
        SELECT B.titre, E.date_emprunt
        FROM Emprunts E
        JOIN Bibliotheque B ON E.livre_id = B.ID_livre
        WHERE E.user_id = ? AND E.date_retour IS NULL
    ''', (user_id,))
    emprunts = cursor.fetchall()
    conn.close()

    return render_template('mes_emprunts.html', emprunts=emprunts)
    
@app.route('/rendre_livre/<int:id_livre>')  # Utilise POST pour éviter de rendre un livre via un lien
def rendre_livre(id_livre):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = sqlite3.connect('database.db')  # Assurez-vous que cette connexion est correcte
    cursor = conn.cursor()

    # Mettre à jour l'emprunt pour ajouter la date de retour
    cursor.execute('UPDATE Emprunts SET date_retour = CURRENT_DATE WHERE livre_id = ? AND user_id = ? AND date_retour IS NULL', (id_livre, user_id))

    # Vérifie si la mise à jour a réussi (c'est-à-dire qu'il y avait un emprunt actif)
    if cursor.rowcount > 0:
        # Réaugmenter la quantité du livre dans la bibliothèque
        cursor.execute('UPDATE Bibliotheque SET quantite = quantite + 1 WHERE ID_livre = ?', (id_livre,))
    
    conn.commit()
    conn.close()

    return redirect('/mes_emprunts')  # Redirige vers la page des emprunts de l'utilisateur


if __name__ == "__main__":
    app.run(debug=True)
