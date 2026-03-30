from flask import Blueprint, render_template, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from functools import wraps
from app.models.models import Eleve, Note, Presence, Bulletin
from app import db
import os
from flask import current_app

eleve_bp = Blueprint('eleve', __name__)


def eleve_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ('eleve', 'admin'):
            flash('Accès réservé aux élèves.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


def get_eleve():
    return Eleve.query.filter_by(user_id=current_user.id).first()


@eleve_bp.route('/dashboard')
@login_required
@eleve_required
def dashboard():
    eleve = get_eleve()
    if not eleve:
        flash('Profil élève introuvable. Contactez l\'administration.', 'warning')
        return redirect(url_for('auth.logout'))

    cours_list = eleve.classe.cours if eleve.classe else []
    recent_notes = Note.query.filter_by(eleve_id=eleve.id).order_by(
        Note.date_ajout.desc()).limit(5).all()

    from datetime import date, timedelta
    from app.models.models import Presence
    threshold_date = date.today() - timedelta(days=30)
    absences = Presence.query.filter_by(eleve_id=eleve.id, present=False).filter(
        Presence.date >= threshold_date).count()
    show_alert = absences > 3

    return render_template('eleve/dashboard.html', eleve=eleve,
                           cours_list=cours_list, recent_notes=recent_notes,
                           absences=absences, show_alert=show_alert)


@eleve_bp.route('/notes')
@login_required
@eleve_required
def notes():
    eleve = get_eleve()
    trimestres = {}
    for t in [1, 2, 3]:
        notes_t = Note.query.filter_by(eleve_id=eleve.id, trimestre=t).all()
        if notes_t:
            notes_avec_valeur = [n for n in notes_t if n.valeur is not None]
            if notes_avec_valeur:
                total_coeff = sum(n.cours.coefficient for n in notes_avec_valeur)
                total_points = sum(n.valeur * n.cours.coefficient for n in notes_avec_valeur)
                moyenne = round(total_points / total_coeff, 2) if total_coeff > 0 else None
            else:
                moyenne = None
            trimestres[t] = {'notes': notes_t, 'moyenne': moyenne}
    return render_template('eleve/notes.html', eleve=eleve, trimestres=trimestres)


@eleve_bp.route('/presences')
@login_required
@eleve_required
def presences():
    eleve = get_eleve()
    presences_list = Presence.query.filter_by(eleve_id=eleve.id).order_by(
        Presence.date.desc()).all()
    total = len(presences_list)
    presents = sum(1 for p in presences_list if p.present)
    taux = round((presents / total * 100), 1) if total > 0 else 0
    return render_template('eleve/presences.html', eleve=eleve,
                           presences=presences_list, taux=taux)


@eleve_bp.route('/bulletins')
@login_required
@eleve_required
def bulletins():
    eleve = get_eleve()
    bulletins_list = Bulletin.query.filter_by(eleve_id=eleve.id).order_by(
        Bulletin.trimestre).all()
    return render_template('eleve/bulletins.html', eleve=eleve, bulletins=bulletins_list)


@eleve_bp.route('/bulletin/<int:bulletin_id>/download')
@login_required
@eleve_required
def download_bulletin(bulletin_id):
    bulletin = db.session.get(Bulletin, bulletin_id)
    if not bulletin:
        flash('Bulletin introuvable.', 'danger')
        return redirect(url_for('eleve.bulletins'))
    eleve = get_eleve()
    if bulletin.eleve_id != eleve.id and current_user.role != 'admin':
        flash('Accès refusé.', 'danger')
        return redirect(url_for('eleve.bulletins'))
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], bulletin.pdf_path)
    if not os.path.exists(path):
        flash('Fichier PDF introuvable. Contactez l\'administration.', 'warning')
        return redirect(url_for('eleve.bulletins'))
    return send_file(path, as_attachment=True,
                     download_name=f'bulletin_T{bulletin.trimestre}.pdf')


@eleve_bp.route('/carte')
@login_required
@eleve_required
def carte():
    eleve = get_eleve()
    return render_template('eleve/carte.html', eleve=eleve)


@eleve_bp.route('/carte/download')
@login_required
@eleve_required
def download_carte():
    eleve = get_eleve()
    path = os.path.join(current_app.config['UPLOAD_FOLDER'],
                        'cartes', f'carte_{eleve.id}.pdf')
    if not os.path.exists(path):
        try:
            from app.utils.pdf_gen import generate_carte_identite
            generate_carte_identite(eleve)
        except Exception as e:
            flash(f'Erreur génération carte : {e}', 'danger')
            return redirect(url_for('eleve.carte'))
    return send_file(path, as_attachment=True,
                     download_name=f'carte_PGB_{eleve.matricule}.pdf')
