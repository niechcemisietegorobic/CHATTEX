import json
import boto3
from botocore.exceptions import ClientError
from .helpers import is_dev

def get_django_secret_key():
    secret_name = f"{"dev" if is_dev() else "prod"}/chattex/django_secret_key"
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="us-east-1"
    )
    try:
        secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e
    secret = json.loads(secret_value_response['SecretString'])['SECRET_KEY']
    return secret

# one invite is always active and is not tied to any user
def get_root_invite():
    secret_name = f"{"dev" if is_dev() else "prod"}/chattex/root_invite"
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="us-east-1"
    )
    try:
        secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e
    secret = json.loads(secret_value_response['SecretString'])['INVITE_CODE']
    return secret

def get_rds_credentials():
    if is_dev():
        secret_name = "rds!db-1f639054-c2d5-49ad-825a-215bde1cb794"
    else:
        secret_name = "rds!db-8b2910b1-7e1d-4238-a860-1fc3ef9769f6"
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="us-east-1"
    )
    try:
        secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e
    secret = json.loads(secret_value_response['SecretString'])
    return secret