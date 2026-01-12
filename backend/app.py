import os
from flask import Flask
from flask_cors import CORS
from models import db
from routes import (
    public_messages_blueprint, private_messages_blueprint, 
    forum_blueprint, auth_blueprint, health_blueprint
    )
from helpers import is_dev
from websock import socket
import boto3
from botocore.exceptions import ClientError

def get_django_secret_key(is_dev: bool = False):
    secret_name = f"{"dev" if is_dev else "prod"}/chattex/django_secret_key"
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="us-east-1"
    )
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e
    secret = get_secret_value_response['SECRET_KEY']
    print(len(secret), "THIS IS A FETCH TEST ---------------<<<<<<<<<<<<<<<<<<<<")
    print("dev" if is_dev else "prod")
    return secret

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = get_django_secret_key(is_dev())

db.init_app(app)
socket.init_app(app)
CORS(app, origins=["https://dev.chattex.cyanjnpr.dev", "https://chattex.cyanjnpr.dev"])

app.register_blueprint(auth_blueprint)
app.register_blueprint(public_messages_blueprint)
app.register_blueprint(private_messages_blueprint)
app.register_blueprint(forum_blueprint)
app.register_blueprint(health_blueprint)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    socket.run(app, host='0.0.0.0', port=5000)
