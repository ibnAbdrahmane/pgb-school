-- =========================================================
--  SCRIPT D'INSTALLATION POUR XAMPP (phpMyAdmin)
--  Exécutez ce script dans phpMyAdmin > onglet SQL
-- =========================================================

-- 1. Créer la base de données
CREATE DATABASE IF NOT EXISTS pgb_school
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- 2. Sélectionner la base
USE pgb_school;

-- 3. (Optionnel) Créer un utilisateur dédié
--    Si vous utilisez root, ignorez cette partie
-- CREATE USER IF NOT EXISTS 'pgb_user'@'localhost' IDENTIFIED BY 'pgb_pass';
-- GRANT ALL PRIVILEGES ON pgb_school.* TO 'pgb_user'@'localhost';
-- FLUSH PRIVILEGES;

-- Les tables sont créées automatiquement par Flask-SQLAlchemy au démarrage.
-- Ce script crée juste la base vide.

SELECT 'Base pgb_school créée avec succès !' AS message;
