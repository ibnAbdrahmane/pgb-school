from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_socketio import emit, join_room
from app import socketio, db
from app.models.models import ChatMessage
from datetime import datetime

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/')
@login_required
def index():
    messages = ChatMessage.query.filter_by(room='general').order_by(
        ChatMessage.timestamp.asc()).limit(100).all()
    return render_template('shared/chat.html', messages=messages)


@socketio.on('connect')
def on_connect():
    if current_user.is_authenticated:
        join_room('general')
        emit('user_joined', {
            'user': current_user.full_name(),
            'role': current_user.role,
            'time': datetime.utcnow().strftime('%H:%M')
        }, room='general')


@socketio.on('send_message')
def handle_message(data):
    if not current_user.is_authenticated:
        return
    message_text = (data.get('message') or '').strip()
    if not message_text or len(message_text) > 1000:
        return

    try:
        msg = ChatMessage(user_id=current_user.id, message=message_text, room='general')
        db.session.add(msg)
        db.session.commit()

        emit('new_message', {
            'id': msg.id,
            'user': current_user.full_name(),
            'role': current_user.role,
            'avatar': current_user.photo,
            'message': message_text,
            'time': msg.timestamp.strftime('%H:%M'),
            'user_id': current_user.id
        }, room='general')
    except Exception as e:
        db.session.rollback()
