from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum('admin', 'prof', 'eleve', 'scolarite'), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    photo = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    prof_profile = db.relationship('Prof', backref='user', uselist=False, cascade='all, delete-orphan')
    eleve_profile = db.relationship('Eleve', backref='user', uselist=False, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def full_name(self):
        fn = self.first_name or ''
        ln = self.last_name or ''
        return f"{fn} {ln}".strip() or self.username


class Classe(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    niveau = db.Column(db.String(50))
    annee_scolaire = db.Column(db.String(10), default='2024-2025')

    eleves = db.relationship('Eleve', backref='classe', lazy=True)
    cours = db.relationship('Cours', backref='classe', lazy=True)


class Prof(db.Model):
    __tablename__ = 'profs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    specialite = db.Column(db.String(100))
    telephone = db.Column(db.String(20))
    matricule = db.Column(db.String(20), unique=True)

    cours = db.relationship('Cours', backref='prof', lazy=True)
    presences = db.relationship('Presence', backref='prof', lazy=True)


class Eleve(db.Model):
    __tablename__ = 'eleves'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    matricule = db.Column(db.String(20), unique=True)
    classe_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    date_naissance = db.Column(db.Date)
    lieu_naissance = db.Column(db.String(100))
    adresse = db.Column(db.String(200))
    telephone_parent = db.Column(db.String(20))
    nom_parent = db.Column(db.String(100))
    photo = db.Column(db.String(200))
    numero_carte = db.Column(db.String(20), unique=True)
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)

    notes = db.relationship('Note', backref='eleve', lazy=True, cascade='all, delete-orphan')
    presences = db.relationship('Presence', backref='eleve', lazy=True)


class Cours(db.Model):
    __tablename__ = 'cours'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20))
    coefficient = db.Column(db.Float, default=1.0)
    classe_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    prof_id = db.Column(db.Integer, db.ForeignKey('profs.id'))

    notes = db.relationship('Note', backref='cours', lazy=True, cascade='all, delete-orphan')
    presences = db.relationship('Presence', backref='cours', lazy=True)


class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleves.id'), nullable=False)
    cours_id = db.Column(db.Integer, db.ForeignKey('cours.id'), nullable=False)
    valeur = db.Column(db.Float)
    type_note = db.Column(db.Enum('devoir', 'examen', 'tp', 'oral'), default='devoir')
    trimestre = db.Column(db.Integer, default=1)
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)
    commentaire = db.Column(db.String(200))

    __table_args__ = (
        db.UniqueConstraint('eleve_id', 'cours_id', 'type_note', 'trimestre',
                            name='uq_note_eleve_cours_type_trim'),
    )


class Presence(db.Model):
    __tablename__ = 'presences'
    id = db.Column(db.Integer, primary_key=True)
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleves.id'), nullable=False)
    cours_id = db.Column(db.Integer, db.ForeignKey('cours.id'), nullable=False)
    prof_id = db.Column(db.Integer, db.ForeignKey('profs.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    present = db.Column(db.Boolean, default=True)
    motif = db.Column(db.String(200))


class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    room = db.Column(db.String(50), default='general')

    user = db.relationship('User', backref='messages')


class Bulletin(db.Model):
    __tablename__ = 'bulletins'
    id = db.Column(db.Integer, primary_key=True)
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleves.id'), nullable=False)
    trimestre = db.Column(db.Integer)
    annee_scolaire = db.Column(db.String(10))
    moyenne_generale = db.Column(db.Float)
    rang = db.Column(db.Integer)
    mention = db.Column(db.String(50))
    pdf_path = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    eleve = db.relationship('Eleve', backref='bulletins')
