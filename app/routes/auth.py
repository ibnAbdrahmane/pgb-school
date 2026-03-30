from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.models import User
from app import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for(f'{current_user.role}.dashboard'))
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(f'{current_user.role}.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        is_carte = request.form.get('is_carte') == '1'
        
        user = None
        if is_carte:
            from app.models.models import Eleve
            eleve = Eleve.query.filter_by(numero_carte=username).first()
            if eleve:
                user = eleve.user
                if user.check_password(password or '1234') and user.is_active:
                    login_user(user)
                    flash(f'Bienvenue {user.full_name()} (carte {username})!', 'success')
                    next_page = request.args.get('next')
                    return redirect(next_page or url_for(f'{user.role}.dashboard'))
        else:
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password) and user.is_active:
                login_user(user)
                flash(f'Bienvenue, {user.full_name()} !', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for(f'{user.role}.dashboard'))
        flash('Identifiants incorrects.', 'danger')
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('auth.login'))
