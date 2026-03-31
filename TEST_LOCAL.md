# 🧪 Test Local avec Docker — Avant de déployer

Avant de déployer sur Railway/Render, testez localement pour vérifier que tout fonctionne.

---

## 1️⃣ Tester en local avec docker-compose

### Vérifier que Docker est installé
```powershell
docker --version
docker-compose --version
```

Si ce n'est pas installé : https://www.docker.com/products/docker-desktop

### Démarrer les services
```powershell
cd c:\xampp\htdocs\pgb-school
docker-compose up --build
```

**Vous devriez voir** :
```
pgb_db is healthy ✓
pgb_redis is healthy ✓
Starting pgb_app...
WARNING: localhost and 127.0.0.1 are not the same
Attaching to pgb_db, pgb_redis, pgb_app
pgb_app | ✅ ============================================
pgb_app | ✅ PGB-School prêt!
```

### Accéder à l'application
Ouvrez dans le navigateur :
```
http://localhost:5000
```

Vous devriez voir la page de connexion ✅

### Tester les fonctionnalités principais

#### 1. Connexion Admin
```
Username: admin
Password: admin123
```
✅ Dashboard admin doit s'afficher

#### 2. Connexion Scolarite
```
Username: scolarite
Password: scolarite123
```
✅ Interface scolarité doit s'afficher

#### 3. Tester le chat (WebSocket)
```
1. Ouvrez 2 onglets : http://localhost:5000
2. Connectez-vous comme admin dans l'onglet 1
3. Connectez-vous comme scolarite dans l'onglet 2
4. Allez à "Chat" dans les 2 onglets
5. Tapez un message dans l'onglet 1
6. Vous devriez voir le message dans l'onglet 2 immédiatement ✅
```

#### 4. Tester les uploads (Photos)
```
1. Allez sur "Scolarité" → "Inscription Elève"
2. Essayez d'uploader une photo
3. Photo doit apparaître dans uploads/ ✅
```

#### 5. Tester la génération PDF
```
1. Scolarité → Inscription Élève → Ajouter un élève
2. Admin → Ajouter notes ou bulletin
3. Tester le lien "Télécharger PDF"
4. Doit générer un PDF sans erreur ✅
```

### Voir les logs
```powershell
# Logs en direct
docker-compose logs -f app

# Logs MySQL
docker-compose logs -f db

# Logs Redis
docker-compose logs -f redis
```

### Arrêter les services
```powershell
docker-compose down
```

Cela arrête les conteneurs SANS supprimer les données.

### Nettoyer complètement
```powershell
docker-compose down -v
```

⚠️ Cela supprime aussi la base de données locale!

---

## 2️⃣ Tester les modifications avant de pusher

Avant de faire `git push` vers GitHub :

```bash
# 1. Arrêter les services existants
docker-compose down

# 2. Reconstruire l'image (prend quelques minutes)
docker-compose up --build

# 3. Tester les fonctionnalités dans le navigateur
# http://localhost:5000

# 4. Vérifier les logs qu'il n'y a pas d'erreurs
docker-compose logs

# 5. Si tout est bon :
git add .
git commit -m "Description de la modif"
git push origin main
```

Railway construira la même image et la déploiera ✅

---

## 3️⃣ Debugger les problèmes localement

### Erreur : "Bind for 0.0.0.0:5000 failed"
```
Le port 5000 est déjà utilisé
Solution : docker-compose down puis relancer
```

### Erreur : "MySQL connection refused"
```
MySQL n'a pas eu le temps de redémarrer
Solution :
- Attendez 30-40 secondes
- Vérifiez : docker-compose logs db
```

### Erreur : "Chat ne fonctionne pas"
```
Redis n'est pas connecté
Solution :
- Vérifiez : docker-compose logs redis
- Assurez-vous que eventlet est en requirements-docker.txt
```

### Erreur : "Static files not found"
```
Les fichiers CSS/JS Bootstrap ne se chargent pas
Solution :
- Vérifiez la console du navigateur (F12)
- Vérifier que __init__.py initialise static/ correctement
```

---

## 4️⃣ Accès à la base de données locale

Si vous voulez inspecter MySQL localement :

### Via Docker
```powershell
docker exec -it pgb_db mysql -u pgb_user -pgb_pass pgb_school
```

Vous êtes maintenant dans MySQL :
```sql
SHOW TABLES;
SELECT * FROM user;
```

### Via HeidiSQL (GUI)
1. Téléchargez : https://www.heidisql.com/
2. Connexion :
   - Hôte : 127.0.0.1
   - Port : 3306
   - Username : pgb_user
   - Password : pgb_pass
   - Database : pgb_school

---

## 5️⃣ Vérifier la taille de l'image Docker

```powershell
docker images
```

Vous devriez voir quelque chose comme :

```
REPOSITORY    TAG      SIZE
pgb_school    latest   ~850MB  (ok, Python 3.11 + libs)
mysql         8.0      ~680MB
redis         7        ~50MB
```

---

## ✅ Checklist de test local

- [ ] `docker-compose up --build` fonctionne sans erreur
- [ ] http://localhost:5000 accessible dans navigateur
- [ ] Connexion admin/admin123 fonctionne
- [ ] Connexion scolarite/scolarite123 fonctionne
- [ ] Dashboard s'affiche correctement
- [ ] Chat WebSocket fonctionne (2 onglets)
- [ ] Upload de photo fonctionne
- [ ] Génération PDF fonctionne
- [ ] Pas d'erreur 500 sur les routes principales
- [ ] `docker-compose down` arrête tout proprement

**Si tout est OK → Prêt pour déployer! 🚀**

---

## 📝 Notes

- Les logs peuvent être bruyants, c'est normal
- Les images Docker causent se télécharger la première fois (~30 sec)
- Redis peut afficher des WARNING, c'est normal en dev
- Les uploads locaux vont dans `uploads/` (à la racine du projet)

---

Pour plus de détails : Voir **DEPLOYMENT_GUIDE.md**
