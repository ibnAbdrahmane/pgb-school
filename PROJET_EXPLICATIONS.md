# Documentation Complète du Projet — Système de Gestion Scolaire PGB-School

## 📖 Aperçu Général du Projet

**PGB-School** est une application web complète de gestion scolaire développée avec **Flask** (Python). Elle permet la gestion complète d'une école avec des espaces dédiés pour différents rôles :

- **Admin** : Gestion des utilisateurs, classes, cours
- **Service Scolarité** : Inscriptions élèves/profs, génération cartes d'identité
- **Professeurs** : Saisie notes/présences, génération bulletins
- **Élèves** : Consultation notes, présences, bulletins, carte d'identité

### Fonctionnalités Principales
- **Authentification & Autorisation** : Rôles multiples avec Flask-Login
- **Gestion Notes & Présences** : Saisie par trimestre, moyennes automatiques
- **Bulletins Scolaires** : Génération PDF automatique (ReportLab)
- **Cartes d'Identité** : QR Code + Photo (Pillow, qrcode)
- **Chat en Temps Réel** : WebSocket multi-utilisateurs (Flask-SocketIO + Redis)
- **Upload Photos** : Caméra ou fichier (sécurisé)
- **Dashboard Personnalisés** : Par rôle avec graphiques et stats

### Accès Démo
| Rôle | Login | Mot de passe |
|------|-------|--------------|
| Admin | `admin` | `admin123` |
| Scolarité | `scolarite` | `scolarite123` |

**URL** : http://localhost:5000

## 🏗️ Architecture & Structure des Fichiers

```
pgb-school/
├── app/
│   ├── __init__.py          # Flask Factory + Extensions (db, login, socketio)
│   ├── models/models.py     # 9 Modèles SQLAlchemy (User, Eleve, Prof, etc.)
│   ├── routes/              # Blueprints par rôle (admin.py, prof.py, etc.)
│   ├── templates/           # Jinja2 + Bootstrap 5
│   ├── utils/
│   │   ├── pdf_gen.py       # Bulletins & Cartes PDF (ReportLab)
│   │   ├── helpers.py       # Fonctions utilitaires
│   │   └── seed.py          # Données initiales (admin/scolarite)
│   └── uploads/             # Photos, PDFs générés
├── run.py                   # Point d'entrée (dev/prod)
├── requirements.txt         # Dépendances locales
├── requirements-docker.txt  # Dépendances Docker
├── docker-compose.yml       # MySQL + Redis + App
├── setup_xampp.sql          # Schema DB
└── README.md / INSTALLATION.md
```

## 🗄️ Modèles de Base de Données (SQLAlchemy)

| Modèle | Description | Relations Principales |
|--------|-------------|----------------------|
| **User** | Utilisateur de base (tous rôles) | Prof/Eleve (1:1), Messages Chat |
| **Eleve** | Profil élève | Classe, Notes, Présences, Bulletins |
| **Prof** | Profil professeur | Cours, Présences |
| **Classe** | Groupe classe | Eleves, Cours |
| **Cours** | Matière | Prof, Classe, Notes, Présences |
| **Note** | Note individuelle | Eleve, Cours (unique par type/trimestre) |
| **Presence** | Pointage | Eleve, Cours, Prof |
| **Bulletin** | Bulletin trimestriel PDF | Eleve |
| **ChatMessage** | Messages chat realtime | User |

**Base** : MySQL 8.0 (utf8mb4), Connexion via PyMySQL.

## 🔧 Bibliothèques Utilisées

### **requirements.txt** (Local/XAMPP)
```
Flask==3.0.3                    # Framework web
Flask-SQLAlchemy==3.1.1         # ORM DB
Flask-Login==0.6.3              # Sessions & Auth
Flask-WTF==1.2.1                # Formulaires sécurisés
Flask-Mail==0.9.1               # Emails (optionnel)
PyMySQL==1.1.1                  # Driver MySQL
Pillow==10.4.0                  # Manipulation images (photos)
reportlab==4.2.2                # Génération PDF bulletins/cartes
python-dotenv==1.0.1            # Variables d'environnement
Werkzeug==3.0.3                 # Utils sécurité (hash mdp)
WTForms==3.1.2                  # Validation formulaires
qrcode==7.4.2                   # QR Codes cartes ID
cryptography==42.0.8            # Chiffrement (fichiers sensibles)
greenlet==3.0.3                 # Compat async
```

### **requirements-docker.txt** (Production)
**+** :
```
eventlet==0.35.2                # Serveur async WSGI
gunicorn==22.0.0                # Serveur production
redis==5.0.8                    # Broker WebSocket
```

### Autres Dépendances Indirectes
- **Jinja2** : Templates HTML (inclus Flask)
- **Bootstrap 5** : Interface responsive
- **FontAwesome** : Icônes
- **Chart.js** : Graphiques dashboard

## 🚀 Modes de Déploiement

### 1. **Local (XAMPP - Windows)**
```
1. XAMPP → Créer DB pgb_school
2. pip install -r requirements.txt
3. python run.py
```

### 2. **Docker (Recommandé)**
```
docker-compose up --build
```
**Services** : App (5000) + MySQL (3306) + Redis (6379)

### 3. **Production**
- Gunicorn + Eventlet (multi-thread async)
- Redis pour SocketIO scalable
- Volumes persistants Docker

## 🔄 Flux d'Utilisation Typique

1. **Admin** → Crée classes/cours/utilisateurs
2. **Scolarité** → Inscrit élèves/profs + Photos → Génère **Cartes ID** (PDF+QR)
3. **Prof** → Saisie **Notes** (par trimestre) + **Présences** → Auto-génère **Bulletins**
4. **Eleve** → Consultation + Téléchargement PDFs
5. **Tous** → **Chat temps réel**

## 📝 Configuration (app/__init__.py)

```python
# DB (XAMPP défaut)
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/pgb_school'

# Uploads
UPLOAD_FOLDER = 'uploads/'  # photos/, bulletins/, cartes/

# SocketIO
# Local : threading
# Docker : eventlet + redis://redis:6379
```

## 🛠️ Scripts Utilitaires (app/utils/)

- **seed.py** : Créé admin/scolarite + classes exemples
- **pdf_gen.py** : Bulletins (notes/moyennes) + Cartes ID (photo/QR)
- **helpers.py** : Calcul moyennes, stats dashboard

## 📊 Fonctionnalités Avancées

| Fonction | Implémentation | Bénéfice |
|----------|----------------|----------|
| **Upload Photo** | Webcam ou fichier | Cartes réalistes |
| **QR Code** | qrcode[pil] | Vérification identité |
| **Chat RT** | SocketIO + Redis | Communication instantanée |
| **PDF Auto** | ReportLab + DB query | Bulletins professionnels |
| **Stats** | SQLAlchemy queries | Dashboards dynamiques |
| **Sécurité** | Flask-Login + Hash | Sessions protégées |

## 🔗 Liens Utiles
- **Dashboard Admin** : /admin/dashboard.html
- **Seeder DB** : `python -c "from app.utils.seed import seed_admin; seed_admin()"`
- **DB Schema** : setup_xampp.sql
- **Support** : Chat intégré !

---

*Généré automatiquement par BLACKBOXAI. Projet prêt pour production !*
