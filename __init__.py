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
@app.route('/emprunt', methods=['POST'])
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
                message = f"Livre avec ISBN {isbn} emprunté avec succès."
            else:
                message = f"Aucun exemplaire disponible pour l'ISBN {isbn}."
        else:
            message = f"Aucun livre trouvé avec l'ISBN {isbn}."
    except Exception as e:
        message = f"Une erreur est survenue : {str(e)}"
    finally:
        conn.close()

    # Retourne le template avec le message
    return render_template('result.html', message=message)


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
