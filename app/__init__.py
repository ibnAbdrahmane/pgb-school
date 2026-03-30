from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
import os

# Charger le fichier .env s'il existe
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()


def create_app():
    app = Flask(__name__)

    # ── Configuration ──────────────────────────────────────────────
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'pgb-dev-secret-2024')

    # Base de données : XAMPP par défaut (root sans mdp)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:@localhost:3306/pgb_school'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

    # Dossier uploads : relatif au dossier racine du projet
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    upload_default = os.path.join(base_dir, 'uploads')
    app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', upload_default)
    # Normaliser le chemin (relatif → absolu)
    if not os.path.isabs(app.config['UPLOAD_FOLDER']):
        app.config['UPLOAD_FOLDER'] = os.path.join(base_dir, app.config['UPLOAD_FOLDER'])

    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    # Créer les sous-dossiers uploads
    for sub in ('photos', 'bulletins', 'cartes'):
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], sub), exist_ok=True)

    # ── Extensions ─────────────────────────────────────────────────
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
    login_manager.login_message_category = 'warning'

    # SocketIO : Redis si disponible, sinon threading (mode local)
    redis_url = os.environ.get('REDIS_URL', '').strip()
    if redis_url:
        # Mode production Docker avec Redis
        socketio.init_app(app, cors_allowed_origins="*",
                          async_mode='eventlet', message_queue=redis_url)
    else:
        # Mode développement local sans Redis
        socketio.init_app(app, cors_allowed_origins="*", async_mode='threading')

    # ── Blueprints ─────────────────────────────────────────────────
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.prof import prof_bp
    from app.routes.eleve import eleve_bp
    from app.routes.scolarite import scolarite_bp
    from app.routes.chat import chat_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(prof_bp, url_prefix='/prof')
    app.register_blueprint(eleve_bp, url_prefix='/eleve')
    app.register_blueprint(scolarite_bp, url_prefix='/scolarite')
    app.register_blueprint(chat_bp, url_prefix='/chat')

    # Importer les événements SocketIO (chat)
    from app.routes import chat as _chat_events  # noqa

    # ── Base de données ────────────────────────────────────────────
    with app.app_context():
        db.create_all()
        from app.utils.seed import seed_admin
        seed_admin()

    return app
