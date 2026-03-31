# 🚀 Démarrage Rapide — PGB-School

## 1️⃣ En local avec Docker (Recommandé)

### Prérequis
- Docker Desktop installé (https://www.docker.com/products/docker-desktop)
- Git installé

### Démarrer en 3 commandes

```bash
# 1. Cloner le projet
git clone https://github.com/votreusername/pgb-school.git
cd pgb-school

# 2. Démarrer les services (MySQL, Redis, App)
docker-compose up --build

# 3. Accéder à l'application
# Ouvrez : http://localhost:5000
```

### Identifiants par défaut
- **Administrateur** : `admin` / `admin123`
- **Scolarité** : `scolarite` / `scolarite123`

---

## 2️⃣ Déployer sur le Cloud (pour partager le lien)

### Option A : Railway (⭐ Recommandé, $5 gratuits/mois)

1. Allez sur **https://railway.app** et inscrivez-vous avec GitHub
2. Créez un nouveau projet → "Deploy from GitHub"
3. Sélectionnez votre dépôt `pgb-school`
4. Ajoutez les services : MySQL + Redis
5. Configurez `SECRET_KEY` dans les variables d'environnement
6. Cliquez "Deploy"

**Votre URL publique** : https://pgb-school-xxx.railway.app

### Option B : Render (Gratuit, mais limité)

1. Inscrivez-vous sur **https://render.com** avec GitHub
2. Créez un Web Service → Sélectionnez votre dépôt
3. Déployez
4. Ajoutez MySQL et Redis
5. Configurez les variables d'environnement

**Votre URL publique** : https://pgb-school.onrender.com

---

## 3️⃣ Mettre à jour après modification

```bash
# Vos modifications locales
git add .
git commit -m "Description de la mise à jour"
git push origin main

# Railway/Render détecte automatiquement et redéploie ✅
```

---

## 🆘 Problèmes courants

| Problème | Solution |
|----------|----------|
| **Port 5000 déjà utilisé** | `docker-compose down && docker-compose up` |
| **Problème de connexion DB** | Vérifiez `docker-compose logs db` |
| **Chat WebSocket ne marche pas** | Vérifiez que Redis est démarré |
| **Uploads ne persistent pas** | En cloud, utilisez S3 (see DEPLOYMENT_GUIDE.md) |

---

## 📚 Documentation complète

👉 Voir [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) pour les détails
