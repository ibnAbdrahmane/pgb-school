import os

# Charger .env avant tout
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from app import create_app, socketio
from flask import send_from_directory, jsonify

app = create_app()


@app.route('/health')
def health_check():
    """Health check endpoint pour Docker/Cloud"""
    try:
        from app import db
        # Vérifier que la DB est accessible
        db.session.execute('SELECT 1')
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 503


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    upload_folder = app.config['UPLOAD_FOLDER']
    return send_from_directory(upload_folder, filename)


if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', '1') == '1'
    socketio.run(app, host='0.0.0.0', port=5000, debug=debug,
                 allow_unsafe_werkzeug=True)

