import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Données pour la table Livres
cur.execute("INSERT INTO Livres (titre, auteur, annee_publication, genre, isbn, nbre_exemplaires) VALUES (?, ?, ?, ?, ?, ?)",
            ('Le Petit Prince', 'Antoine de Saint-Exupéry', 1943, 'Fiction', '978-3-16-148410-0', '5'))
cur.execute("INSERT INTO Livres (titre, auteur, annee_publication, genre, isbn, nbre_exemplaires) VALUES (?, ?, ?, ?, ?, ?)",
            ('1984', 'George Orwell', 1949, 'Dystopie', '978-0-452-28423-4', '2'))
cur.execute("INSERT INTO Livres (titre, auteur, annee_publication, genre, isbn, nbre_exemplaires) VALUES (?, ?, ?, ?, ?, ?)",
            ('Les Misérables', 'Victor Hugo', 1862, 'Classique', '978-0-14-044430-8', '7'))

# Données pour la table Utilisateurs
cur.execute("INSERT INTO Utilisateurs (nom, prenom, email, date_inscription, mot_de_passe, role) VALUES (?, ?, ?, ?, ?, ?)",
            ('Dupont', 'Emilie', 'emilie.dupont@example.com', '2023-01-15', 'motdepasse', 'emprunteur'))
cur.execute("INSERT INTO Utilisateurs (nom, prenom, email, date_inscription, mot_de_passe, role) VALUES (?, ?, ?, ?, ?, ?)",
            ('Martin', 'Jean', 'jean.martin@example.com', '2023-02-10', 'motdepasse', 'emprunteur'))
cur.execute("INSERT INTO Utilisateurs (nom, prenom, email, date_inscription, mot_de_passe, role) VALUES (?, ?, ?, ?, ?, ?)",
            ('Durand', 'Sophie', 'sophie.durand@example.com', '2023-03-20', 'motdepasse', 'emprunteur'))


# Données pour la table Emprunts
cur.execute("INSERT INTO Emprunts (id_utilisateur, id_livre, date_emprunt, date_retour_prevue, date_retour_effective) VALUES (?, ?, ?, ?, ?)",
            (1, 1, '2025-01-01', '2025-01-15', None))
cur.execute("INSERT INTO Emprunts (id_utilisateur, id_livre, date_emprunt, date_retour_prevue, date_retour_effective) VALUES (?, ?, ?, ?, ?)",
            (2, 2, '2025-01-05', '2025-01-20', None))
cur.execute("INSERT INTO Emprunts (id_utilisateur, id_livre, date_emprunt, date_retour_prevue, date_retour_effective) VALUES (?, ?, ?, ?, ?)",
            (3, 3, '2025-01-10', '2025-01-25', None))

connection.commit()
connection.close()
