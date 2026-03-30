from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from functools import wraps
from app.models.models import User, Eleve, Prof, Classe, Cours, Note
from app import db
import base64
import os
import uuid

scolarite_bp = Blueprint('scolarite', __name__)


def scolarite_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ('scolarite', 'admin'):
            flash('Accès réservé au service scolarité.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@scolarite_bp.route('/dashboard')
@login_required
@scolarite_required
def dashboard():
    stats = {
        'eleves': Eleve.query.count(),
        'profs': Prof.query.count(),
        'classes': Classe.query.count(),
    }
    recent_eleves = Eleve.query.order_by(Eleve.date_inscription.desc()).limit(6).all()
    return render_template('scolarite/dashboard.html', stats=stats, recent_eleves=recent_eleves)


@scolarite_bp.route('/eleves')
@login_required
@scolarite_required
def eleves():
    classe_id = request.args.get('classe_id', type=int)
    query = Eleve.query
    if classe_id:
        query = query.filter_by(classe_id=classe_id)
    eleves_list = query.all()
    classes = Classe.query.all()
    return render_template('scolarite/eleves.html', eleves=eleves_list,
                           classes=classes, selected_classe=classe_id)


@scolarite_bp.route('/add-eleve', methods=['GET', 'POST'])
@login_required
@scolarite_required
def add_eleve():
    classes = Classe.query.all()
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()

        if not username or not email or not first_name or not last_name:
            flash('Tous les champs obligatoires doivent être remplis.', 'danger')
            return render_template('scolarite/add_eleve.html', classes=classes)

        if User.query.filter_by(username=username).first():
            flash("Ce nom d'utilisateur existe déjà.", 'danger')
            return render_template('scolarite/add_eleve.html', classes=classes)

        if User.query.filter_by(email=email).first():
            flash("Cet email est déjà utilisé.", 'danger')
            return render_template('scolarite/add_eleve.html', classes=classes)

        user = User(username=username, email=email, role='eleve',
                    first_name=first_name, last_name=last_name)
        pwd = request.form.get('password', '').strip() or 'pgb1234'
        user.set_password(pwd)

        photo_data = request.form.get('photo_data', '')
        if photo_data and photo_data.startswith('data:image'):
            user.photo = _save_photo(photo_data, username)

        db.session.add(user)
        db.session.flush()

        from app.utils.helpers import generate_matricule, generate_numero_carte
        classe_id = request.form.get('classe_id') or None
        dn = request.form.get('date_naissance', '').strip() or None
        eleve = Eleve(
            user_id=user.id,
            matricule=generate_matricule(user.id),
            numero_carte=generate_numero_carte(user.id),
            classe_id=int(classe_id) if classe_id else None,
            date_naissance=dn,
            lieu_naissance=request.form.get('lieu_naissance', ''),
            adresse=request.form.get('adresse', ''),
            telephone_parent=request.form.get('telephone_parent', ''),
            nom_parent=request.form.get('nom_parent', ''),
            photo=user.photo
        )
        db.session.add(eleve)
        db.session.flush()

        try:
            from app.utils.pdf_gen import generate_carte_identite
            generate_carte_identite(eleve)
        except Exception as e:
            flash(f'Avertissement carte PDF : {e}', 'warning')

        db.session.commit()
        flash(f'Élève {first_name} {last_name} inscrit avec succès !', 'success')
        return redirect(url_for('scolarite.eleves'))

    return render_template('scolarite/add_eleve.html', classes=classes)


@scolarite_bp.route('/profs')
@login_required
@scolarite_required
def profs():
    profs_list = Prof.query.all()
    return render_template('scolarite/profs.html', profs=profs_list)


@scolarite_bp.route('/add-prof', methods=['GET', 'POST'])
@login_required
@scolarite_required
def add_prof():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()

        if not username or not email or not first_name or not last_name:
            flash('Tous les champs obligatoires doivent être remplis.', 'danger')
            return render_template('scolarite/add_prof.html')

        if User.query.filter_by(username=username).first():
            flash("Ce nom d'utilisateur existe déjà.", 'danger')
            return render_template('scolarite/add_prof.html')

        if User.query.filter_by(email=email).first():
            flash("Cet email est déjà utilisé.", 'danger')
            return render_template('scolarite/add_prof.html')

        user = User(username=username, email=email, role='prof',
                    first_name=first_name, last_name=last_name)
        pwd = request.form.get('password', '').strip() or 'pgb1234'
        user.set_password(pwd)

        photo_data = request.form.get('photo_data', '')
        if photo_data and photo_data.startswith('data:image'):
            user.photo = _save_photo(photo_data, username)

        db.session.add(user)
        db.session.flush()

        prof = Prof(user_id=user.id,
                    specialite=request.form.get('specialite', ''),
                    telephone=request.form.get('telephone', ''),
                    matricule=f"PR{user.id:04d}")
        db.session.add(prof)
        db.session.commit()

        flash(f'Professeur {first_name} {last_name} ajouté !', 'success')
        return redirect(url_for('scolarite.profs'))

    return render_template('scolarite/add_prof.html')


@scolarite_bp.route('/cours')
@login_required
@scolarite_required
def cours():
    all_cours = Cours.query.all()
    return render_template('scolarite/cours.html', cours=all_cours)


@scolarite_bp.route('/notes')
@login_required
@scolarite_required
def notes():
    classe_id = request.args.get('classe_id', type=int)
    classes = Classe.query.all()
    notes_data = []
    if classe_id:
        classe = db.session.get(Classe, classe_id)
        if classe:
            for eleve in classe.eleves:
                eleve_notes = Note.query.filter_by(eleve_id=eleve.id).all()
                notes_data.append({'eleve': eleve, 'notes': eleve_notes})
    return render_template('scolarite/notes.html', classes=classes,
                           notes_data=notes_data, selected_classe=classe_id)


@scolarite_bp.route('/cartes')
@login_required
@scolarite_required
def cartes():
    from app.models.models import Eleve
    eleves = Eleve.query.order_by(Eleve.date_inscription.desc()).all()
    return render_template('scolarite/cartes.html', eleves=eleves)


@scolarite_bp.route('/download-carte/<int:eleve_id>')
@login_required
@scolarite_required
def download_carte(eleve_id):
    from app.models.models import Eleve
    eleve = Eleve.query.get(eleve_id)
    if not eleve:
        flash('Élève introuvable.', 'danger')
        return redirect(url_for('scolarite.cartes'))
    
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'cartes', f'carte_{eleve.id}.pdf')
    if not os.path.exists(path):
        try:
            from app.utils.pdf_gen import generate_carte_identite
            generate_carte_identite(eleve)
        except Exception as e:
            flash(f'Erreur génération PDF : {e}', 'danger')
            return redirect(url_for('scolarite.cartes'))
    
    return send_file(path, as_attachment=True, download_name=f'carte_PGB_{eleve.matricule}.pdf')


def _save_photo(data, username):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    try:
        header, encoded = data.split(',', 1)
        img_bytes = base64.b64decode(encoded)
        filename = f"{username}_{uuid.uuid4().hex[:8]}.jpg"
        path = os.path.join(upload_folder, 'photos', filename)
        with open(path, 'wb') as f:
            f.write(img_bytes)
        return f"photos/{filename}"
    except Exception as e:
        current_app.logger.error(f"Erreur sauvegarde photo: {e}")
        return None
