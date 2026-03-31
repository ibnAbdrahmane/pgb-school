# 📦 Guide de Déploiement — PGB-School sur Railway/Render

## 🚀 Prérequis

- ✅ Compte **GitHub** (gratuit sur github.com)
- ✅ Compte **Railway.app** (gratuit, avec $5 crédits/mois)
  - OU Compte **Render.com** (gratuit avec limitations)
- ✅ Git installé localement

---

## 📋 Étape 1 : Préparer le projet pour GitHub

### 1.1 Créer un dépôt GitHub

1. Allez sur **https://github.com/new**
2. Créez un nouveau dépôt : `pgb-school`
3. Copiez l'URL du dépôt (par ex: `https://github.com/votreusername/pgb-school.git`)

### 1.2 Initialiser Git localement

```bash
cd c:\xampp\htdocs\pgb-school
git init
git add .
git commit -m "Initial commit: PGB-School Flask application"
git branch -M main
git remote add origin https://github.com/votreusername/pgb-school.git
git push -u origin main
```

### 1.3 Ignorer les fichiers sensibles (créer `.gitignore`)

```
# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/
env/
pip-log.txt

# Flask
instance/
.webassets-cache

# IDE
.vscode/
.idea/
*.swp

# Uploads (données locales)
uploads/
!uploads/.gitkeep

# Environment
.env
.env.local

# Database
*.db
*.sqlite
```

---

## 🚀 Option A : Déploiement sur Railway (Recommandé ⭐)

### Avantages
✅ Très facile (1-2 clics)
✅ $5 crédits gratuits/mois (suffisant pour un petit projet)
✅ Support natif Docker
✅ MySQL, Redis, et App dans l'interface
✅ Déploiement automatique depuis GitHub

### Étapes

#### 1. S'inscrire sur Railway

1. Allez sur **https://railway.app**
2. Cliquez sur "Sign Up" → Connectez-vous avec GitHub

#### 2. Créer un projet Railway

1. Cliquez sur "New Project" → "Deploy from GitHub repo"
2. Autorisez Railway à accéder à votre GitHub
3. Sélectionnez le dépôt `pgb-school`
4. Railway détecte le Dockerfile automatiquement ✅

#### 3. Ajouter les services

**MySQL Database:**
1. Dans le tableau de bord Railway, cliquez sur "Add Service"
2. Recherchez "MySQL"
3. Déployez (Railway crée la base de données et génère `DATABASE_URL`)

**Redis:**
1. Cliquez sur "Add Service" → "Redis"
2. Déployez

**Application:**
1. Configurez les variables d'environnement :
   - `SECRET_KEY`: Générez une clé sécurisée (ex: `openssl rand -hex 32`)
   - `FLASK_ENV`: `production`
   - `DATABASE_URL`: Sera auto-générée par Railway
   - `REDIS_URL`: Sera auto-générée par Railway
   - `UPLOAD_FOLDER`: `/app/uploads`

2. Cliquez sur "Deploy" → Railway construit et déploie automatiquement

#### 4. Accéder à votre application

1. Allez dans **Deployments** de Railway
2. Cliquez sur l'URL du service `app`
3. Vous avez votre application accessible au public! 🎉

**URL publique** : `https://pgb-school-xxx.railway.app`

---

## 🚀 Option B : Déploiement sur Render.com

### Avantages
✅ Interface intuitive
✅ Gratuit (avec Web Service 0.5 CPU / 512 MB)
⚠️ Services MySQL/Redis gratuits → suspendus après 90 jours d'inactivité

### Étapes

#### 1. S'inscrire

Allez sur **https://render.com** → Sign Up avec GitHub

#### 2. Créer un nouveau Web Service

1. Cliquez sur "New+" → "Web Service"
2. Sélectionnez le dépôt `pgb-school`
3. Configurez :
   - **Name** : `pgb-school`
   - **Environment** : `Docker`
   - **Build Command** : (laissez vide, Render utilise le Dockerfile)
   - **Start Command** : (laissez vide, Render utilise le CMD du Dockerfile)

#### 3. Ajouter MySQL et Redis

1. Cliquez sur "New+" → "MySQL"
   - Copez la `DATABASE_URL` générée
2. Cliquez sur "New+" → "Redis"
   - Copez la `REDIS_URL` générée

#### 4. Configurer les variables d'environnement

Allez dans l'onglet **Environment** du Web Service et ajoutez :

```
SECRET_KEY=votre-clé-sécurisée
FLASK_ENV=production
DATABASE_URL=mysql://user:pass@host/dbname
REDIS_URL=redis://user:pass@host:port
UPLOAD_FOLDER=/app/uploads
```

#### 5. Déployer

Render déploie automatiquement depuis GitHub. Votre URL :

**https://pgb-school.onrender.com**

---

## 🔄 Déploiements futurs

### Mise à jour automatique depuis GitHub

1. Railway et Render se reconstruisent **automatiquement** chaque fois que vous faites un `git push main`
2. Pour déployer une mise à jour :

```bash
git add .
git commit -m "Description de la mise à jour"
git push origin main
```

3. Railroad/Render détecte le changement et redéploie automatiquement ✅

---

## 🛡️ Configuration pour la Production

### Variables d'environnement importantes

| Variable | Exemple | Importance |
|----------|---------|-----------|
| `SECRET_KEY` | `abc123def456...` | 🔴 Générez une clé forte (32+ caractères) |
| `FLASK_ENV` | `production` | 🔴 Toujours `production` |
| `DATABASE_URL` | `mysql://...` | 🔴 Généré automatiquement par Railway/Render |
| `REDIS_URL` | `redis://...` | 🟡 Généré automatiquement |
| `UPLOAD_FOLDER` | `/app/uploads` | 🟡 Pour Docker |

### Générer une clé secrète forte

**Linux/Mac** :
```bash
openssl rand -hex 32
```

**Windows PowerShell** :
```powershell
[System.Convert]::ToHexString((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
```

**Ou en ligne** : https://randomkeygen.com/ (CodeIgniter → 32 caractères)

---

## 📁 Structure des uploads Docker

Les uploads (photos, bulletins, cartes ID) sont stockés dans `/app/uploads` à l'intérieur du conteneur.

**Important** : Les volumes Docker utilisés dans `docker-compose.yml` :
```yaml
volumes:
  uploads_data:/app/uploads
```

En production (Railway/Render), cela fonctionne avec un stockage persistant.

---

## 🐛 Dépannage

### Problème : "Bad Gateway" / Erreur 502

**Solution** :
1. Vérifiez que `DATABASE_URL` est correcte
2. Vérifiez que MySQL peut être atteint depuis l'app
3. Consultez les **Logs** (onglet Deployments dans Railway)

### Problème : Uploads qui disparaissent

**Solution** : Utilisez un service de stockage externe :
- **Railway** : Intégration S3 automatique
- **Render** : Ajouter un bucket AWS S3 manuel

### Problème : WebSocket (Chat) ne fonctionne pas

**Solution** :
1. Vérifiez que `eventlet` et `gunicorn` sont dans `requirements-docker.txt` ✅
2. Vérifiez que `REDIS_URL` est configurée
3. Redis doit être accessible depuis l'app

---

## 📊 Coûts estimés

| Service | Railway | Render |
|---------|---------|--------|
| **App** | $0 (dans les $5 crédits/mois) | $0 (gratuit) |
| **MySQL** | $0 (dans les crédits) | $0 (gratuit, 90j inactivité) |
| **Redis** | $0 (dans les crédits) | $0 (gratuit, 90j inactivité) |
| **Stockage uploads** | Inclus | Limité, SVP utiliser S3 |
| **Total/mois** | **$0-5** | **$0** |

---

## ✅ Checklist de déploiement

- [ ] Compte GitHub créé et dépôt `pgb-school` créé
- [ ] Code poussé vers `main` avec `git push`
- [ ] Compte Railway.app créé (ou Render.com)
- [ ] Services MySQL et Redis déployés
- [ ] Variables d'environnement configurées
- [ ] Application déployée et URL accessible
- [ ] Connexion possible avec admin/admin123
- [ ] Chat WebSocket fonctionne (tester dans 2 onglets)
- [ ] Uploads photos possibles
- [ ] Génération PDF bulletins/cartes ID fonctionne

---

## 🎉 Partage du lien

Une fois déployé(e), partagez simplement l'URL :

**Railway** : `https://pgb-school-xxx.railway.app`
**Render** : `https://pgb-school.onrender.com`

L'autre personne peut :
1. Accéder à votre application sans rien installer
2. Se connecter avec les comptes démo (admin/admin123, scolarite/scolarite123)
3. Tester toutes les fonctionnalités

---

## 📞 Support

- **Railway Docs** : https://docs.railway.app
- **Render Docs** : https://render.com/docs
- **Flask-SocketIO sur Docker** : https://flask-socketio.readthedocs.io
