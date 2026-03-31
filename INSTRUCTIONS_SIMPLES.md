# 🎯 Instructions Simplifiées — Déployer votre projet pour le partager

**Résumé**: Vous allez mettre votre code sur GitHub, puis les utiliser pour déployer automatiquement sur Railroad. Voici comment en 10 minutes.

---

## 📍 Étape 1 : Créer des comptes (5 min)

### 1a. Compte GitHub (Où héberger votre code)
1. Allez sur **https://github.com/signup**
2. Créez un compte avec votre email
3. Notez votre **username** (ex: `jean2024`)

### 1b. Compte Railway (Où déployer - GRATUIT!)
1. Allez sur **https://railway.app**
2. Cliquez "Sign Up"
3. Connectez-vous avec votre compte GitHub
4. Autorisez Railway à accéder à votre GitHub

✅ **Vous avez les 2 comptes!**

---

## 📤 Étape 2 : Créer un dépôt sur GitHub (2 min)

1. Dans GitHub, allez sur **https://github.com/new**
2. **Repository name** : `pgb-school`
3. **Description** : "Système de gestion scolaire"
4. Cliquez **"Create repository"**
5. **Copez l'URL** qui s'affiche (ex: `https://github.com/votreususername/pgb-school.git`)

✅ **Votre dépôt GitHub est créé!**

---

## 💾 Étape 3 : Pousser votre code (2 min)

### Sur Windows (Ouvrir PowerShell)

```powershell
# 1. Aller dans votre dossier du projet
cd c:\xampp\htdocs\pgb-school

# 2. Initialiser Git dans le dossier
git init

# 3. Ajouter TOUS les fichiers
git add .

# 4. Créer un "snapshot" de votre code
git commit -m "Premier commit: PGB-School"

# 5. Renommer la branche en "main"
git branch -M main

# 6. Ajouter votre dépôt GitHub (REMPLACEZ votreusername!)
git remote add origin https://github.com/votreusername/pgb-school.git

# 7. Envoyer votre code sur GitHub
git push -u origin main
```

**Vous verrez**:
```
Enumerating objects: ...
Counting objects: ...
...
To https://github.com/votreusername/pgb-school.git
 * [new branch]      main -> main
```

✅ **Votre code est maintenant sur GitHub!**

---

## 🚀 Étape 4 : Déployer avec Railway (3 min)

### Dans Railway (https://railway.app)

1. Cliquez **"New Project"**
2. Sélectionnez **"Deploy from GitHub repo"**
3. Vous verrez une liste de vos repos
4. Cliquez sur **"pgb-school"**
5. Autorisez Railway si demandé
6. Railway commence à construire... **Attendez ~3 min** ⏳

**Pendant ce temps**, Railway:
- Récupère votre code
- Crée l'image Docker
- Démarre les conteneurs

---

## ⚙️ Étape 5 : Ajouter les bases de données (1 min)

### Dans le dashboard Railway

1. Cliquez **"Add Service"** (bouton +)
2. Cherchez **"MySQL"** → Cliquez
3. Déployez (Railway fait tout automatiquement)
   - Une base de données est créée
   - Une `DATABASE_URL` est générée

4. Refait la même chose pour **"Redis"**
   - Cliquez **"Add Service"**
   - Cherchez **"Redis"** → Cliquez
   - Déployez

✅ **MySQL et Redis sont déployés!**

---

## 🔧 Étape 6 : Configurer les variables (2 min)

### Dans Railway, allez sur le service "app"

1. Cliquez sur l'onglet **"Variables"**
2. Ajoute ces variables:

```
SECRET_KEY = pgb-production-key-2024
FLASK_ENV = production
UPLOAD_FOLDER = /app/uploads
```

**Les autres variables** (DATABASE_URL, REDIS_URL) **sont générées automatiquement** ✅

---

## 🎉 Étape 7 : Votre application est en ligne!

### Obtenir l'URL

1. Dans Railway éloignez sur **"Deployments"**
2. Cliquez sur le lien du service **"app"**
3. Vous avez une URL comme:

```
https://pgb-school-abc123.railway.app
```

**Vous pouvez partager ce lien!** 🎊

---

## 📱 Comment partager avec quelqu'un d'autre

Donnez-lui simplement le lien:

```
https://pgb-school-abc123.railway.app

Identifiants (à donner):
- Admin: admin / admin123
- Scolarité: scolarite / scolarite123
```

Cette personne peut:
- ✅ Accéder depuis n'importe quel ordinateur
- ✅ Pas besoin d'installer quoi que ce soit
- ✅ Tout fonctionne dans le navigateur
- ✅ Utiliser les fonctionnalités complètes

---

## 🔄 Comment mettre à jour après (Futur)

Si vous modifiez votre code:

```powershell
cd c:\xampp\htdocs\pgb-school

# Ajouter vos modifications
git add .

# Créer un snapshot
git commit -m "Ma modification"

# Envoyer à GitHub
git push origin main
```

**Railway le voit automatiquement et redéploie!** ✅

---

## 🆘 Problèmes courants

| Problème | Solution |
|----------|----------|
| **Erreur lors du déploiement** | Regardez les "Logs" dans Railway |
| **Erreur 502 (Bad Gateway)** | Attendez 2 min, faire F5 dans le navigateur |
| **Du peut se connecter** | Vérifiez admin/admin123 |
| **Chat ne marche pas** | Attendez que Redis soit prêt (~1 min) |
| **Database error** | Attendez que MySQL soit prêt (~1 min) |

---

## 📞 Besoin d'aide?

Consultez ces fichiers du projet:
- **QUICK_START.md** — Vue d'ensemble
- **DEPLOYMENT_GUIDE.md** — Guide détaillé
- **TEST_LOCAL.md** — Tester avant de déployer

---

## ✅ Récapitulatif

```
GitHub (votre code)
       ↓ (git push)
    Railway (construction automatique)
       ↓
  Docker Image construite
       ↓
  Conteneurs lancés (App + MySQL + Redis)
       ↓
  URL publique généré
       ↓
  Vous pouvez partager le lien!
```

---

**C'est tout! Votre projet est maintenant accessible en ligne.** 🎉

Vous pouvez partager le lien avec quiconque pour qu'il accède à votre application scolaire.
