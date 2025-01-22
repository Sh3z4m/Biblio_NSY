from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)                                                                                                                  

# Page accueil
@app.route('/')
def hello_world():
    return render_template('display_all.html')


# Tout avant cette ligne !
if __name__ == "__main__":
  app.run(debug=True)
