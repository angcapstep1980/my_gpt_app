import sys
sys.dont_write_bytecode=True
from flask import Flask, render_template, request, jsonify, make_response, g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model import get_database_uri
from controller import call_llm
import uuid
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}  # evita disconnessioni
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELLI DB ---
class Session(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), db.ForeignKey('session.id'), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# --- GESTIONE SESSIONE ---
@app.before_request
def load_session():
    session_id = request.cookies.get('session_id')
    if not session_id or not Session.query.get(session_id):
        session_id = str(uuid.uuid4())
        db.session.add(Session(id=session_id))
        db.session.commit()
        g.new_session_id = session_id
    g.session_id = session_id

@app.after_request
def set_session_cookie(response):
    if hasattr(g, 'new_session_id'):
        response.set_cookie('session_id', g.new_session_id, httponly=True, max_age=30*24*60*60)
    return response

# --- API ---
@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').strip()
    temperature = float(request.json.get('slider_value', '0.0').strip())
    if not user_message:
        return jsonify({'error': 'Messaggio vuoto'}), 400
    session_id = g.session_id
    db.session.add(Message(session_id=session_id, role='user', content=user_message))
    history = Message.query.filter_by(session_id=session_id).order_by(Message.timestamp).all()
    history_list = [{'role': m.role, 'content': m.content} for m in history]
    assistant_reply = call_llm(history_list, temperature)
    db.session.add(Message(session_id=session_id, role='assistant', content=assistant_reply))
    db.session.commit()
    return jsonify({'reply': assistant_reply})

@app.route('/api/history', methods=['GET'])
def get_history():
    messages = Message.query.filter_by(session_id=g.session_id).order_by(Message.timestamp).all()
    return jsonify([{'role': m.role, 'content': m.content} for m in messages])

@app.route('/api/reset', methods=['POST'])
def reset_session():
    response = make_response(jsonify({'status': 'ok'}))
    response.set_cookie('session_id', '', expires=0)
    return response

# --- FRONTEND ---
@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )