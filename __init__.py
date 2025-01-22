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
