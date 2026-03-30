# 🚀 Guide d'installation — École PGB

---

## Option A — Lancement local avec XAMPP (Windows)

### Étape 1 : Créer la base de données

1. Démarrer **XAMPP** (Apache + MySQL)
2. Ouvrir **phpMyAdmin** → http://localhost/phpmyadmin
3. Cliquer sur **"SQL"** et coller :
   ```sql
   CREATE DATABASE IF NOT EXISTS pgb_school CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
4. Cliquer **"Exécuter"**

### Étape 2 : Configurer le fichier .env

Le fichier `.env` est déjà créé. Par défaut il utilise `root` sans mot de passe (config XAMPP standard).

Si votre MySQL a un mot de passe root, éditez `.env` :
```
DATABASE_URL=mysql+pymysql://root:VOTRE_MOT_DE_PASSE@localhost:3306/pgb_school
```

### Étape 3 : Installer les dépendances Python

```bash
# Dans le dossier pgb-school :
pip install -r requirements.txt
```

> ⚠️ **Windows** : Si `cryptography` échoue, essayez :
> ```bash
> pip install --upgrade pip
> pip install cryptography --no-binary cryptography
> ```

### Étape 4 : Lancer l'application

```bash
python run.py
```

Accéder à : **http://localhost:5000**

| Rôle | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Scolarité | `scolarite` | `scolarite123` |

---

## Option B — Docker (déploiement complet)

### Prérequis
- Docker Desktop installé

### Lancement
```bash
docker-compose up --build
```

L'application sera disponible sur **http://localhost:5000**

> La base de données est automatiquement créée et configurée.

### Arrêter
```bash
docker-compose down
```

### Arrêter et supprimer les données
```bash
docker-compose down -v
```

---

## 🔧 Dépannage fréquent

| Erreur | Solution |
|--------|----------|
| `Access denied for user 'pgb_user'` | Vérifiez `DATABASE_URL` dans `.env` |
| `Unknown database 'pgb_school'` | Créer la DB dans phpMyAdmin (Étape 1) |
| `ModuleNotFoundError: eventlet` | Normal en local — `eventlet` n'est pas dans `requirements.txt` |
| Port 5000 déjà utilisé | Changer le port dans `run.py` : `port=5001` |
| `mysqlclient` ne s'installe pas | Normal — on utilise `PyMySQL` à la place |
