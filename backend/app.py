import os
from flask import Flask
from flask_cors import CORS
from models import db
from routes import (
    public_messages_blueprint, private_messages_blueprint, 
    forum_blueprint, auth_blueprint, health_blueprint,
    settings_blueprint
    )
from helpers import get_django_secret_key, get_rds_credentials, limiter, check_environment
from websock import socket

if (not check_environment()):
    raise RuntimeError("environment is not configured correctly")

app = Flask(__name__)
rds_credentials = get_rds_credentials()
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@{}:5432/chattex".format(
    rds_credentials.get("username"), rds_credentials.get("password"), 
    os.environ.get('RDS_URL'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = get_django_secret_key()

db.init_app(app)
socket.init_app(app)
limiter.init_app(app)
CORS(app, origins=[os.environ.get("FRONTEND_URL")])

app.register_blueprint(auth_blueprint)
app.register_blueprint(public_messages_blueprint)
app.register_blueprint(private_messages_blueprint)
app.register_blueprint(forum_blueprint)
app.register_blueprint(health_blueprint)
app.register_blueprint(settings_blueprint)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    print("run in a container, quitting...")
