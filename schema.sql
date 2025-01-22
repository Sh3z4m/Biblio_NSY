-- Table pour les livres
CREATE TABLE Livres (
    id_livre INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(255) NOT NULL,
    auteur VARCHAR(255) NOT NULL,
    annee_publication YEAR,
    genre VARCHAR(100),
    isbn VARCHAR(20) UNIQUE
);

-- Table pour les utilisateurs
CREATE TABLE Utilisateurs (
    id_utilisateur INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    date_inscription DATE DEFAULT CURRENT_DATE
);

-- Table pour les stocks
CREATE TABLE Stocks (
    id_stock INT AUTO_INCREMENT PRIMARY KEY,
    id_livre INT NOT NULL,
    quantite_disponible INT DEFAULT 0,
    FOREIGN KEY (id_livre) REFERENCES Livres(id_livre) ON DELETE CASCADE
);

-- Table pour les emprunts
CREATE TABLE Emprunts (
    id_emprunt INT AUTO_INCREMENT PRIMARY KEY,
    id_utilisateur INT NOT NULL,
    id_livre INT NOT NULL,
    date_emprunt DATE DEFAULT CURRENT_DATE,
    date_retour_prevue DATE,
    date_retour_effective DATE,
    FOREIGN KEY (id_utilisateur) REFERENCES Utilisateurs(id_utilisateur) ON DELETE CASCADE,
    FOREIGN KEY (id_livre) REFERENCES Livres(id_livre) ON DELETE CASCADE
);

-- Index pour faciliter la recherche de livres disponibles
CREATE INDEX idx_livres_disponibles ON Stocks (id_livre, quantite_disponible);

-- Exemple de recherche de livres disponibles
-- SELECT l.titre, l.auteur, s.quantite_disponible
-- FROM Livres l
-- JOIN Stocks s ON l.id_livre = s.id_livre
-- WHERE s.quantite_disponible > 0;
