# 🏫 École PGB — Système de Gestion Scolaire

Application web **Flask** complète pour la gestion d'une école, avec espaces distincts pour l'admin, les professeurs, les élèves et le service scolarité.

[![GitHub](https://img.shields.io/badge/GitHub-pgb--school-blue)](https://github.com)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-blue)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Supported-brightgreen)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)

---

## 🚀 Démarrage Rapide

### 📦 En local avec Docker

```bash
# 1. Cloner le projet
git clone https://github.com/votreusername/pgb-school.git
cd pgb-school

# 2. Démarrer (MySQL, Redis, App)
docker-compose up --build

# 3. Ouvrir dans le navigateur
# http://localhost:5000
```

### ☁️ Déploié sur le Cloud

👉 **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** — Guide complet pour Railway/Render

### 📱 Accès Demo

| Rôle | Username | Password | Rôle |
|------|----------|----------|------|
| Administrateur | `admin` | `admin123` | Gestion complète |
| Service Scolarité | `scolarite` | `scolarite123` | Inscriptions |
| Professeur | `prof` | `prof123` | Notas/Présences |
| Élève | `eleve` | `eleve123` | Consultation |

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [QUICK_START.md](./QUICK_START.md) | Démarrage en 3 étapes |
| [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) | Déployer on Railway/Render |
| [PROJET_EXPLICATIONS.md](./PROJET_EXPLICATIONS.md) | Documentation technique complète |
| [INSTALLATION.md](./INSTALLATION.md) | Installation sur XAMPP/Serveur |

---

## 🎯 Fonctionnalités Principales

### 👨‍💼 Administrateur
✅ Gestion complète des utilisateurs (CRUD)
✅ Création/modification des classes et cours
✅ Accès à tout l'espace
✅ Statistiques globales

### 📚 Service Scolarité
✅ Inscription des élèves avec photo (caméra + import)
✅ Génération automatique cartes d'identité scolaire (PDF + QR Code)
✅ Gestion des professeurs
✅ Consultation des notes et cours

### 👨‍🏫 Professeurs
✅ Saisie notes par cours/trimestre
✅ Pointage automatique des présences
✅ Génération bulletins quand notes complètes
✅ Dashboard avec statistiques

### 👨‍🎓 Élèves
✅ Consultation des notes (par trimestre + moyenne)
✅ Historique des présences
✅ Téléchargement des bulletins PDF
✅ Visualisation carte d'identité
✅ Chat temps réel avec les camarades

### 💬 Chat Temps Réel
✅ WebSocket pour conversations instantanées
✅ Multi-utilisateurs
✅ Historique persistant en base de données

---

## 🏗️ Architecture & Technologie

### Stack Technique
- **Backend** : Flask 3.0.3 (Python 3.11)
- **Frontend** : Bootstrap 5 + Jinja2 templates
- **Base de données** : MySQL 8.0
- **Cache/WebSocket** : Redis 7
- **Authentification** : Flask-Login (Sessions)
- **PDF** : ReportLab (Bulletins & Cartes ID)
- **Temps réel** : Flask-SocketIO + Eventlet
- **Déploiement** : Docker + docker-compose

### Structure du Projet
```
pgb-school/
├── app/
│   ├── __init__.py              # Flask Factory
│   ├── models/
│   │   └── models.py            # 9 modèles SQLAlchemy
│   ├── routes/
│   │   ├── auth.py              # Authentification
│   │   ├── admin.py             # Admin routes
│   │   ├── prof.py              # Prof routes
│   │   ├── eleve.py             # Élève routes
│   │   ├── scolarite.py         # Scolarite routes
│   │   └── chat.py              # WebSocket chat
│   ├── templates/               # HTML + Jinja2
│   └── utils/
│       ├── pdf_gen.py           # Génération PDF
│       ├── helpers.py           # Utilitaires
│       └── seed.py              # Données initiales
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.py
└── README.md
```

### Modèles de Base de Données
| Modèle | Utilité |
|--------|---------|
| **User** | Utilisateur (tous rôles) |
| **Eleve** | Profil élève + photo |
| **Prof** | Profil professeur |
| **Classe** | Groupe classe |
| **Cours** | Matière + professeur |
| **Note** | Note par élève/cours/trimestre |
| **Presence** | Pointage journalier |
| **Bulletin** | Bulletin trimestriel PDF |
| **ChatMessage** | Messages WebSocket |

---

## 🐳 Services Docker

| Service | Image | Port | Stockage |
|---------|-------|------|----------|
| **app** | Python 3.11 | 5000 | Uploads (POL) |
| **db** | MySQL 8.0 | 3306 | Volume `db_data` |
| **redis** | Redis 7 | 6379 | En mémoire |

**Réseau** : Bridge `pgb_network` pour la communication inter-conteneurs

---

## 💾 Données Persistantes

### Stockage Local (docker-compose)
```yaml
volumes:
  db_data:       # Données MySQL
  uploads_data:  # Photos, PDFs, cartes
```

### En Cloud (Railway/Render)
- ✅ MySQL géré par Railway/Render
- ✅ Redis managé
- ⚠️ Uploads stockés localement (limité)
- 🔄 Optionnel : Intégrer AWS S3 pour les uploads

---

## ⚙️ Installation & Configuration

### Prérequis
- Docker Desktop ou Docker CLI
- Git
- Navigateur moderne (Chrome, Firefox, Edge)

### Enviro

nement (.env)
```bash
# Production (Railway/Render)
SECRET_KEY=votre-clé-secrète-32-caractères
FLASK_ENV=production
DATABASE_URL=mysql://user:pass@host/db
REDIS_URL=redis://host:port/0
UPLOAD_FOLDER=/app/uploads

# Local (XAMPP)
SECRET_KEY=pgb-dev-secret-2024
FLASK_ENV=development
DATABASE_URL=mysql+pymysql://root:@localhost/pgb_school
REDIS_URL=redis://localhost:6379/0
```

---

## 🔄 Mises à Jour & Déploiement

### Depuis GitHub (Auto-déploiement)
```bash
# Après modification locale
git add .
git commit -m "Description de la mise à jour"
git push origin main

# Railway/Render détecte et redéploie automatiquement ✅
```

### Manuellement en local
```bash
docker-compose down
docker-compose up --build
```

---

## 🛡️ Sécurité

✅ Authentification multi-rôles avec Flask-Login
✅ Hashage des mots de passe (Werkzeug)
✅ Protection CSRF (Flask-WTF)
✅ Validation des uploads (Pillow sécurisée)
✅ SQLAlchemy ORM (Protection SQL Injection)
✅ HTTPS en production (Railway/Render)

---

## 🚀 Déploiement Production

### Railway (Recommandé ⭐)
- $5 crédits gratuits/mois
- 1-2 clics pour déployer
- Voir [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)

### Render
- Gratuit avec limitations
- Services MySQL/Redis suspendus après 90j inactivité
- Voir [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)

### Azure/AWS/GCP
- Plus complexe
- Pour haute disponibilité
- Voir [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)

---

## 📞 Support & Contribution

- 📚 **Docs** : Voir les fichiers `.md` du projet
- 🐛 **Issues** : Signalez les bugs sur GitHub
- 💡 **Améliorations** : Les PRs sont bienvenues!

---

## 📄 Licence

MIT

---

**Made with ❤️ for School Management** | [Déployer maintenant →](./DEPLOYMENT_GUIDE.md)


### Chat en direct
- WebSocket via Flask-SocketIO + Redis
- Messages temps réel pour tous les utilisateurs
- Indicateurs de rôle sur chaque message

## 🌐 Aspect réseau

- **Redis** : Message queue pour SocketIO distribué (permet multi-instances)
- **Docker bridge network** : Communication sécurisée entre conteneurs
- **WebSocket** : Communication bidirectionnelle temps réel
- **REST API** : Toutes les actions via requêtes HTTP standard

## 📦 Publication Docker Hub

```bash
docker build -t username/pgb-school:latest .
docker push username/pgb-school:latest
```

### GitHub Actions CI/CD

```yaml
# .github/workflows/docker.yml
name: Docker CI
on:
  push:
    branches: [ main ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          push: true
          tags: username/pgb-school:latest
```

## 🛠️ Technologies utilisées

| Technologie | Rôle |
|------------|------|
| Flask | Framework web Python |
| Flask-SQLAlchemy | ORM base de données |
| Flask-SocketIO | WebSocket temps réel |
| Flask-Login | Gestion sessions |
| MySQL | Base de données relationnelle |
| Redis | Message broker pour WebSocket |
| ReportLab | Génération PDF (bulletins, cartes) |
| Docker Compose | Orchestration multi-conteneurs |
| Gunicorn + Eventlet | Serveur WSGI async |
