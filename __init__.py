from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__) 
app.secret_key = 'votre_clé_secrète'

# Connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par nom
    return conn

# Routes pour l'authentification
@app.route('/login', methods=['GET', 'POST'])
def auth_login():
    if request.method == 'POST':
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute("SELECT * FROM Utilisateurs WHERE email = ? AND mot_de_passe = ?", (email, mot_de_passe))
        utilisateur = cur.fetchone()
        connection.close()
        if utilisateur:
            session['user_id'] = utilisateur['id_utilisateur']
            session['nom'] = utilisateur['nom']
            session['role'] = utilisateur['role']
            # flask("Connexion réussie.", "success")
            return redirect('/dashboard')
        else:
            flash("Identifiants incorrects.", "danger")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('/'))  # Si l'utilisateur n'est pas connecté, rediriger vers la page de connexion

    # Connexion à la base de données pour récupérer des informations utilisateur
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Utilisateurs WHERE id_utilisateur = ?', (session['user_id'],))
    utilisateur = cursor.fetchone()
    conn.close()

    return render_template('dashboard.html', utilisateur=utilisateur)

@app.route('/logout')
def logout():
    session.clear()  # Déconnecte l'utilisateur
    return redirect(url_for('login'))

# Afficher tous les livres
@app.route('/')
def all_books():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres;')
    data = cursor.fetchall()
    conn.close()
    return render_template('display_all_2.html', data=data)

# Emprunter
@app.route('/', methods=['POST'])
def emprunt():
    try:
        # Récupération de l'ISBN depuis le formulaire
        isbn = request.form.get('emprunt', None)
        if not isbn:
            return render_template('result.html', message="ISBN non fourni dans le formulaire.")      
        # Connexion à la base de données
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Vérification si le livre existe
        cursor.execute('SELECT nbre_exemplaires FROM livres WHERE isbn = ?', (isbn,))
        livre = cursor.fetchone()
        if livre:
            nbre_exemplaires = int(livre[0])
            if nbre_exemplaires > 0:
                # Mise à jour du stock
                cursor.execute('UPDATE livres SET nbre_exemplaires = nbre_exemplaires - 1 WHERE isbn = ?', (isbn,))
                conn.commit()
                message = f"<p style='color:green'>Livre avec ISBN {isbn} emprunté avec succès.</p>"
            else:
                message = f"<p style='color:orange'>Aucun exemplaire disponible pour l'ISBN {isbn}.</p>"
        else:
            message = f"<p style='color:orange'>Aucun livre trouvé avec l'ISBN {isbn}.</p>"
    except Exception as e:
        message = f"<p style='color:red'>Une erreur est survenue : {str(e)}</p>"
    finally:
        conn.close()

    # Retourne le template avec le message
    return render_template('display_all_2.html', message=message)

@app.route('/suppression', methods=['POST'])
def suppressionlivre():
    try:
        # Récupération de l'ISBN depuis le formulaire
        isbn = request.form.get('suppression', None)
        if not isbn:
            return render_template('result.html', message="<p style='color:red'>ISBN non fourni dans le formulaire.</p>")      
        
        # Connexion à la base de données
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Suppression du livre dans la base
        cursor.execute('DELETE FROM livres WHERE isbn = ?', (isbn,))
        conn.commit()  # Sauvegarde des changements
        message = f"<p style='color:green'>Livre avec ISBN {isbn} <b>supprimé</b> avec succès.</p>"
    except Exception as e:
        # Gestion des erreurs
        message = f"<p style='color:red'>Une erreur est survenue : {str(e)}</p>"
    finally:
        # Assurez-vous que la connexion est toujours fermée
        conn.close()

    # Retourne le template avec le message
    return render_template('display_all_2.html', message=message)

# Afficher tous les livres
@app.route('/enregistrer/')
def enregistrer():
    return render_template('enregistrer_2.html')

# Afficher tous les livres
@app.route('/enregistrer/', methods=['POST'])
def enregistrer_post():
    exemplaires = request.form['exemplaires']
    titre = request.form['titre']
    auteur = request.form['auteur']
    annee = request.form['annee']
    genre = request.form['genre']
    isbn = request.form['isbn']


    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Exécution de la requête SQL pour insérer un nouveau client
    cursor.execute('INSERT INTO livres (titre, auteur, annee_publication, genre, isbn, nbre_exemplaires) VALUES (?, ?, ?, ?, ?, ?)', (titre, auteur, annee, genre, isbn, exemplaires))
    conn.commit()
    conn.close()
    return redirect('/')  # Rediriger vers la page d'accueil après l'enregistrement

# Afficher tous les livres
@app.route('/rechercher/')
def rechercher():
    return render_template('rechercher.html')

# # Routes pour la gestion des emprunts
# @app.route('/emprunts', methods=['GET', 'POST'])
# @login_required
# def emprunts():
#     connection = get_db_connection()
#     cur = connection.cursor()
#     if request.method == 'POST':
#         id_utilisateur = session['user_id']
#         id_livre = request.form['livre']
#         cur.execute("INSERT INTO emprunts (id_utilisateur, id_livre, date_retour_prevue) VALUES (?, ?, date('now', '+7 days'))",
#                     (id_utilisateur, id_livre))
#         cur.execute("UPDATE livres SET stock = stock - 1 WHERE id = ?", (id_livre,))
#         connection.commit()
#         flash("Emprunt ajouté avec succès.", "success")
#     cur.execute("""
#         SELECT e.id, u.nom AS utilisateur, l.titre AS livre, e.date_retour_prevue, e.statut
#         FROM emprunts e
#         JOIN utilisateurs u ON e.id_utilisateur = u.id
#         JOIN livres l ON e.id_livre = l.id
#     """)
#     emprunts = cur.fetchall()
#     cur.execute("SELECT * FROM utilisateurs")
#     utilisateurs = cur.fetchall()
#     cur.execute("SELECT * FROM livres WHERE stock > 0")
#     livres = cur.fetchall()
#     connection.close()
#     return render_template('emprunts.html', emprunts=emprunts, utilisateurs=utilisateurs, livres=livres)


# @app.route('/emprunts/retourner/<int:emprunt_id>')
# @login_required
# def retourner_emprunt(emprunt_id):
#     connection = get_db_connection()
#     cur = connection.cursor()
#     cur.execute("UPDATE emprunts SET statut = 'Retourné', date_retour_effective = date('now') WHERE id = ?", (emprunt_id,))
#     cur.execute("UPDATE livres SET stock = stock + 1 WHERE id = (SELECT id_livre FROM emprunts WHERE id = ?)", (emprunt_id,))
#     connection.commit()
#     connection.close()
#     flash("Livre retourné avec succès.", "success")
#     return redirect(url_for('emprunts'))

# Tout avant cette ligne !
if __name__ == "__main__":
  app.run(debug=True)
