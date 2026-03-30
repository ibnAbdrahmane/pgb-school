from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from functools import wraps
from app.models.models import User, Prof, Eleve, Classe, Cours, Note, Bulletin
from app import db
import os
import base64
import uuid

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Accès réservé aux administrateurs.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    stats = {
        'eleves': Eleve.query.count(),
        'profs': Prof.query.count(),
        'classes': Classe.query.count(),
        'cours': Cours.query.count(),
    }
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_eleves = Eleve.query.order_by(Eleve.date_inscription.desc()).limit(6).all()
    return render_template('admin/dashboard.html', stats=stats, recent_users=recent_users, recent_eleves=recent_eleves)


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    all_users = User.query.order_by(User.role, User.last_name).all()
    return render_template('admin/users.html', users=all_users)


@admin_bp.route('/add-user', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    classes = Classe.query.all()
    if request.method == 'POST':
        role = request.form.get('role')
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()

        if not role or not username or not email or not password:
            flash('Tous les champs obligatoires doivent être remplis.', 'danger')
            return render_template('admin/add_user.html', classes=classes)

        if User.query.filter_by(username=username).first():
            flash("Ce nom d'utilisateur existe déjà.", 'danger')
            return render_template('admin/add_user.html', classes=classes)

        if User.query.filter_by(email=email).first():
            flash("Cet email est déjà utilisé.", 'danger')
            return render_template('admin/add_user.html', classes=classes)

        user = User(username=username, email=email, role=role,
                    first_name=first_name, last_name=last_name)
        user.set_password(password)

        # Gestion photo (caméra ou import)
        photo_data = request.form.get('photo_data', '')
        if photo_data and photo_data.startswith('data:image'):
            photo_path = _save_photo_base64(photo_data, username)
            user.photo = photo_path

        db.session.add(user)
        db.session.flush()  # pour avoir user.id

        if role == 'prof':
            matricule = f"PR{user.id:04d}"
            prof = Prof(user_id=user.id,
                        specialite=request.form.get('specialite', ''),
                        telephone=request.form.get('telephone', ''),
                        matricule=matricule)
            db.session.add(prof)

        elif role == 'eleve':
            from app.utils.helpers import generate_matricule, generate_numero_carte
            classe_id = request.form.get('classe_id') or None
            if classe_id:
                classe_id = int(classe_id)
            dn = request.form.get('date_naissance', '').strip() or None
            eleve = Eleve(
                user_id=user.id,
                matricule=generate_matricule(user.id),
                numero_carte=generate_numero_carte(user.id),
                classe_id=classe_id,
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
        flash(f'Utilisateur {first_name} {last_name} créé avec succès !', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/add_user.html', classes=classes)


@admin_bp.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        flash('Utilisateur introuvable.', 'danger')
        return redirect(url_for('admin.users'))
    classes = Classe.query.all()

    if request.method == 'POST':
        user.first_name = request.form.get('first_name', user.first_name)
        user.last_name = request.form.get('last_name', user.last_name)
        new_email = request.form.get('email', '').strip()
        if new_email and new_email != user.email:
            existing = User.query.filter_by(email=new_email).first()
            if existing and existing.id != user.id:
                flash('Cet email est déjà utilisé.', 'danger')
                return render_template('admin/edit_user.html', user=user, classes=classes)
            user.email = new_email
        pwd = request.form.get('password', '').strip()
        if pwd:
            user.set_password(pwd)

        photo_data = request.form.get('photo_data', '')
        if photo_data and photo_data.startswith('data:image'):
            photo_path = _save_photo_base64(photo_data, user.username)
            user.photo = photo_path
            if user.eleve_profile:
                user.eleve_profile.photo = photo_path

        if user.role == 'prof' and user.prof_profile:
            user.prof_profile.specialite = request.form.get('specialite', '')
            user.prof_profile.telephone = request.form.get('telephone', '')
        elif user.role == 'eleve' and user.eleve_profile:
            classe_id = request.form.get('classe_id') or None
            user.eleve_profile.classe_id = int(classe_id) if classe_id else None
            user.eleve_profile.telephone_parent = request.form.get('telephone_parent', '')
            user.eleve_profile.nom_parent = request.form.get('nom_parent', '')

        db.session.commit()
        flash('Utilisateur modifié avec succès !', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/edit_user.html', user=user, classes=classes)


@admin_bp.route('/delete-user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        flash('Utilisateur introuvable.', 'danger')
        return redirect(url_for('admin.users'))
    if user.id == current_user.id:
        flash('Vous ne pouvez pas supprimer votre propre compte.', 'danger')
        return redirect(url_for('admin.users'))
    db.session.delete(user)
    db.session.commit()
    flash('Utilisateur supprimé.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/classes')
@login_required
@admin_required
def classes():
    all_classes = Classe.query.order_by(Classe.niveau).all()
    return render_template('admin/classes.html', classes=all_classes)


@admin_bp.route('/add-classe', methods=['POST'])
@login_required
@admin_required
def add_classe():
    nom = request.form.get('nom', '').strip()
    niveau = request.form.get('niveau', '').strip()
    annee = request.form.get('annee_scolaire', '2024-2025').strip()
    if not nom:
        flash('Le nom de la classe est obligatoire.', 'danger')
        return redirect(url_for('admin.classes'))
    classe = Classe(nom=nom, niveau=niveau, annee_scolaire=annee)
    db.session.add(classe)
    db.session.commit()
    flash(f'Classe {nom} créée !', 'success')
    return redirect(url_for('admin.classes'))


@admin_bp.route('/cours')
@login_required
@admin_required
def cours():
    all_cours = Cours.query.all()
    classes = Classe.query.all()
    profs = Prof.query.all()
    return render_template('admin/cours.html', cours=all_cours, classes=classes, profs=profs)


@admin_bp.route('/cartes')
@login_required
@admin_required
def cartes():
    from app.models.models import Eleve
    eleves = Eleve.query.order_by(Eleve.date_inscription.desc()).all()
    return render_template('admin/cartes.html', eleves=eleves)


@admin_bp.route('/download-carte/<int:eleve_id>')
@login_required
@admin_required
def download_carte(eleve_id):
    from app.models.models import Eleve
    eleve = Eleve.query.get(eleve_id)
    if not eleve:
        flash('Élève introuvable.', 'danger')
        return redirect(url_for('admin.cartes'))
    
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'cartes', f'carte_{eleve.id}.pdf')
    if not os.path.exists(path):
        try:
            from app.utils.pdf_gen import generate_carte_identite
            generate_carte_identite(eleve)
        except Exception as e:
            flash(f'Erreur génération PDF : {e}', 'danger')
            return redirect(url_for('admin.cartes'))
    
    return send_file(path, as_attachment=True, download_name=f'carte_PGB_{eleve.matricule}.pdf')


@admin_bp.route('/add-cours', methods=['POST'])
@login_required
@admin_required
def add_cours():
    nom = request.form.get('nom', '').strip()
    if not nom:
        flash('Le nom du cours est obligatoire.', 'danger')
        return redirect(url_for('admin.cours'))
    classe_id = request.form.get('classe_id') or None
    prof_id = request.form.get('prof_id') or None
    coeff = request.form.get('coefficient', '1.0')
    try:
        coeff = float(coeff)
    except ValueError:
        coeff = 1.0
    c = Cours(
        nom=nom,
        code=request.form.get('code', '').strip(),
        coefficient=coeff,
        classe_id=int(classe_id) if classe_id else None,
        prof_id=int(prof_id) if prof_id else None,
    )
    db.session.add(c)
    db.session.commit()
    flash('Cours ajouté !', 'success')
    return redirect(url_for('admin.cours'))


def _save_photo_base64(data, username):
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
