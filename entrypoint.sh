#!/bin/bash
# ==========================================
# Script de démarrage pour Docker
# Crée les tables de base de données
# ==========================================

set -e

echo "🚀 Démarrage de PGB-School..."
echo "⏳ Attente de la base de données..."

# Attendre que MySQL soit prêt
python3 -c "
import sys
import time
import pymysql

def wait_for_mysql(host='db', user='pgb_user', password='pgb_pass', db='pgb_school', timeout=30):
    start_time = time.time()
    while True:
        try:
            conn = pymysql.connect(host=host, user=user, password=password, database=db)
            conn.close()
            print('✅ MySQL est prêt!')
            return True
        except pymysql.Error as e:
            if time.time() - start_time > timeout:
                print(f'❌ MySQL timeout après {timeout}s', file=sys.stderr)
                return False
            print('⏳ Réessai de connexion à MySQL...', file=sys.stderr)
            time.sleep(2)

sys.exit(0 if wait_for_mysql() else 1)
"

echo "💾 Initialisation de la base de données..."

python3 << 'EOF'
from app import create_app, db
from app.models.models import User, Eleve, Prof, Classe, Cours, Note, Presence, Bulletin, ChatMessage
from app.utils.seed import seed_initial_data

app = create_app()
with app.app_context():
    # Créer les tables
    db.create_all()
    print("✅ Tables de base de données créées")
    
    # Insérer les données initiales
    seed_initial_data()
    print("✅ Données initiales insérées")
EOF

echo ""
echo "✅ ============================================"
echo "✅ PGB-School prêt!"
echo "✅ URL: http://localhost:5000"
echo "✅ Admin: admin / admin123"
echo "✅ Scolarité: scolarite / scolarite123"
echo "✅ ============================================"
echo ""

# Lancer l'application
exec gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 run:app
