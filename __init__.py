from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)                                                                                                                  

# Afficher tous les livres
@app.route('/')
def all_books():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres;')
    data = cursor.fetchall()
    conn.close()
    return render_template('display_all.html', data=data)

# Emprunter
@app.route('/', methods=['GET'])
def emprunt():
    # Récupération de l'ISBN envoyé par le formulaire
    isbn = request.form['emprunt']
    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Vérification si le livre avec cet ISBN existe et récupération du stock
    cursor.execute('SELECT nbre_exemplaires FROM livres WHERE isbn = ?', (isbn,))
    livre = cursor.fetchone()
    if livre:
        nbre_exemplaires = livre[0]
        if nbre_exemplaires > 0:
            # Mise à jour : réduction du stock de 1
            cursor.execute('UPDATE livres SET nbre_exemplaires = nbre_exemplaires - 1 WHERE isbn = ?', (isbn,))
            conn.commit()
            message = f"Livre avec ISBN {isbn} emprunté avec succès."
        else:
            message = f"Aucun exemplaire disponible pour l'ISBN {isbn}."
    else:
        message = f"Aucun livre trouvé avec l'ISBN {isbn}."

    # Fermeture de la connexion
    conn.close()

    # Retourne un template ou un message de confirmation
    return render_template('display_all.html', message=message)

# Afficher tous les livres
@app.route('/enregistrer/')
def emprunter():
    return render_template('enregistrer_2.html')

# Afficher tous les livres
@app.route('/rechercher/')
def rechercher():
    return render_template('rechercher.html')

# Tout avant cette ligne !
if __name__ == "__main__":
  app.run(debug=True)
