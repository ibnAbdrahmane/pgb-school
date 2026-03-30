# École PGB — Système de Gestion Scolaire

Application web Flask complète pour la gestion d'une école, avec espaces distincts pour l'admin, les professeurs, les élèves et le service scolarité.

## 🚀 Démarrage rapide (Docker)

```bash
git clone <repo-url>
cd pgb-school
docker-compose up --build
```

Accéder à : **http://localhost:5000**

### Comptes par défaut
| Rôle | Username | Password |
|------|----------|----------|
| Administrateur | `admin` | `admin123` |
| Service Scolarité | `scolarite` | `scolarite123` |

---

## 🏗️ Architecture

```
pgb-school/
├── app/
│   ├── __init__.py          # Factory Flask + SocketIO
│   ├── models/              # SQLAlchemy models
│   ├── routes/              # Blueprints par rôle
│   │   ├── auth.py
│   │   ├── admin.py
│   │   ├── prof.py
│   │   ├── eleve.py
│   │   ├── scolarite.py
│   │   └── chat.py          # WebSocket chat
│   ├── utils/
│   │   ├── pdf_gen.py       # Génération bulletins & cartes
│   │   ├── helpers.py       # Utilitaires
│   │   └── seed.py          # Données initiales
│   └── templates/           # Jinja2 templates
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── run.py
```

## 🐳 Services Docker

| Service | Image | Port |
|---------|-------|------|
| app | Python 3.11 | 5000 |
| db | MySQL 8.0 | 3306 (interne) |
| redis | Redis 7 | 6379 (interne) |

Le réseau Docker `pgb_network` (bridge) permet la communication entre les conteneurs.

## ✨ Fonctionnalités

### Admin
- Gestion complète des utilisateurs (CRUD)
- Création de classes et cours
- Accès à tout l'espace

### Service Scolarité
- Inscription des élèves avec photo (caméra ou import)
- Génération automatique de la carte d'identité scolaire (PDF)
- Ajout de professeurs
- Consultation des notes et cours

### Professeurs
- Saisie et modification des notes par cours/trimestre
- Pointage des présences
- Génération automatique des bulletins quand toutes les notes sont saisies

### Élèves
- Consultation des notes par trimestre avec moyenne
- Historique des présences
- Téléchargement des bulletins PDF
- Visualisation et téléchargement de la carte d'identité scolaire

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
