from app.models.models import User, Classe
from app import db


def seed_admin():
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@pgb.sn',
            role='admin',
            first_name='Administrateur',
            last_name='PGB',
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)

    if not User.query.filter_by(username='scolarite').first():
        sc = User(
            username='scolarite',
            email='scolarite@pgb.sn',
            role='scolarite',
            first_name='Service',
            last_name='Scolarité',
            is_active=True
        )
        sc.set_password('scolarite123')
        db.session.add(sc)

    # Default classes
    for nom, niveau in [('6ème A', '6ème'), ('5ème A', '5ème'), ('4ème A', '4ème'),
                         ('3ème A', '3ème'), ('2nde A', '2nde'), ('1ère A', '1ère'), ('Terminale A', 'Terminale')]:
        if not Classe.query.filter_by(nom=nom).first():
            db.session.add(Classe(nom=nom, niveau=niveau))

    db.session.commit()
