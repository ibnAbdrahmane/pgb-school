-- Création de la base de données PGB
CREATE DATABASE IF NOT EXISTS pgb_school
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Créer l'utilisateur et lui donner les droits
CREATE USER IF NOT EXISTS 'pgb_user'@'%' IDENTIFIED BY 'pgb_pass';
GRANT ALL PRIVILEGES ON pgb_school.* TO 'pgb_user'@'%';
FLUSH PRIVILEGES;

USE pgb_school;
