from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from app.models.models import Prof, Eleve, Cours, Note, Presence, Classe, Bulletin
from app import db
from datetime import date

prof_bp = Blueprint('prof', __name__)


def prof_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ('prof', 'admin'):
            flash('Accès réservé aux professeurs.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


def get_prof():
    return Prof.query.filter_by(user_id=current_user.id).first()


@prof_bp.route('/dashboard')
@login_required
@prof_required
def dashboard():
    prof = get_prof()
    cours_list = []
    if prof:
        cours_list = Cours.query.filter_by(prof_id=prof.id).all()
        total_eleves = sum(len(c.classe.eleves) for c in cours_list if c.classe) if cours_list else 0
    else:
        cours_list = []
        total_eleves = 0
    return render_template('prof/dashboard.html', prof=prof, cours_list=cours_list, total_eleves=total_eleves)


@prof_bp.route('/notes')
@login_required
@prof_required
def notes():
    prof = get_prof()
    cours_list = Cours.query.filter_by(prof_id=prof.id).all() if prof else []
    selected_cours_id = request.args.get('cours_id', type=int)
    selected_trimestre = request.args.get('trimestre', 1, type=int)
    eleves_notes = []

    if selected_cours_id:
        cours = db.session.get(Cours, selected_cours_id)
        if cours and cours.classe:
            for eleve in cours.classe.eleves:
                note = Note.query.filter_by(
                    eleve_id=eleve.id,
                    cours_id=selected_cours_id,
                    trimestre=selected_trimestre
                ).first()
                eleves_notes.append({'eleve': eleve, 'note': note})

    return render_template('prof/notes.html',
                           cours_list=cours_list,
                           eleves_notes=eleves_notes,
                           selected_cours_id=selected_cours_id,
                           selected_trimestre=selected_trimestre)


@prof_bp.route('/save-notes', methods=['POST'])
@login_required
@prof_required
def save_notes():
    cours_id = request.form.get('cours_id', type=int)
    trimestre = request.form.get('trimestre', 1, type=int)
    type_note = request.form.get('type_note', 'devoir')

    for key, value in request.form.items():
        if key.startswith('note_'):
            try:
                eleve_id = int(key.split('_')[1])
            except (IndexError, ValueError):
                continue
            try:
                valeur = float(value) if value.strip() else None
            except ValueError:
                continue
            if valeur is not None and (valeur < 0 or valeur > 20):
                continue  # ignorer les valeurs hors plage

            existing = Note.query.filter_by(
                eleve_id=eleve_id, cours_id=cours_id,
                type_note=type_note, trimestre=trimestre
            ).first()

            if existing:
                existing.valeur = valeur
            else:
                if valeur is not None:
                    note = Note(eleve_id=eleve_id, cours_id=cours_id,
                                valeur=valeur, type_note=type_note, trimestre=trimestre)
                    db.session.add(note)

    try:
        db.session.commit()
        flash('Notes enregistrées avec succès !', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de l\'enregistrement : {e}', 'danger')
        return redirect(url_for('prof.notes', cours_id=cours_id, trimestre=trimestre))

    # Vérifier si les bulletins peuvent être générés
    cours = db.session.get(Cours, cours_id)
    if cours and cours.classe:
        try:
            _check_and_generate_bulletins(cours.classe.id, trimestre)
        except Exception as e:
            flash(f'Avertissement bulletin : {e}', 'warning')

    return redirect(url_for('prof.notes', cours_id=cours_id, trimestre=trimestre))


@prof_bp.route('/presences')
@login_required
@prof_required
def presences():
    prof = get_prof()
    cours_list = Cours.query.filter_by(prof_id=prof.id).all() if prof else []
    selected_cours_id = request.args.get('cours_id', type=int)
    selected_date = request.args.get('date', date.today().isoformat())
    eleves_presences = []

    if selected_cours_id:
        cours = db.session.get(Cours, selected_cours_id)
        if cours and cours.classe:
            for eleve in cours.classe.eleves:
                presence = Presence.query.filter_by(
                    eleve_id=eleve.id,
                    cours_id=selected_cours_id,
                    date=selected_date
                ).first()
                eleves_presences.append({'eleve': eleve, 'presence': presence})

    return render_template('prof/presences.html',
                           cours_list=cours_list,
                           eleves_presences=eleves_presences,
                           selected_cours_id=selected_cours_id,
                           selected_date=selected_date)


@prof_bp.route('/save-presences', methods=['POST'])
@login_required
@prof_required
def save_presences():
    prof = get_prof()
    if not prof:
        flash('Profil professeur introuvable.', 'danger')
        return redirect(url_for('prof.presences'))
    cours_id = request.form.get('cours_id', type=int)
    selected_date = request.form.get('date', date.today().isoformat())
    presences_data = request.form.getlist('present')

    cours = db.session.get(Cours, cours_id)
    if cours and cours.classe:
        for eleve in cours.classe.eleves:
            existing = Presence.query.filter_by(
                eleve_id=eleve.id, cours_id=cours_id, date=selected_date
            ).first()
            present = str(eleve.id) in presences_data
            if existing:
                existing.present = present
            else:
                p = Presence(eleve_id=eleve.id, cours_id=cours_id,
                             prof_id=prof.id, date=selected_date, present=present)
                db.session.add(p)

    db.session.commit()
    flash('Présences enregistrées !', 'success')
    return redirect(url_for('prof.presences', cours_id=cours_id, date=selected_date))


def _check_and_generate_bulletins(classe_id, trimestre):
    from app.utils.pdf_gen import generate_bulletin
    classe = db.session.get(Classe, classe_id)
    if not classe or not classe.cours:
        return
    total_cours = len(classe.cours)
    if total_cours == 0:
        return
    for eleve in classe.eleves:
        notes_count = Note.query.join(Cours).filter(
            Cours.classe_id == classe_id,
            Note.eleve_id == eleve.id,
            Note.trimestre == trimestre
        ).count()
        if notes_count >= total_cours:
            existing = Bulletin.query.filter_by(
                eleve_id=eleve.id, trimestre=trimestre
            ).first()
            if not existing:
                generate_bulletin(eleve.id, trimestre)
