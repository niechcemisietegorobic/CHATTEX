import os
from flask import Flask
from flask_cors import CORS
from models import db
from routes import (
    public_messages_blueprint, private_messages_blueprint, 
    forum_blueprint, auth_blueprint, health_blueprint,
    settings_blueprint
    )
from helpers import get_django_secret_key, is_dev
from websock import socket

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = get_django_secret_key()

db.init_app(app)
socket.init_app(app)
if (is_dev): CORS(app, origins=["https://dev.chattex.cyanjnpr.dev"])
else: CORS(app, origins=["https://chattex.cyanjnpr.dev"])

app.register_blueprint(auth_blueprint)
app.register_blueprint(public_messages_blueprint)
app.register_blueprint(private_messages_blueprint)
app.register_blueprint(forum_blueprint)
app.register_blueprint(health_blueprint)
app.register_blueprint(settings_blueprint)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    socket.run(app, host='0.0.0.0', port=5000)
