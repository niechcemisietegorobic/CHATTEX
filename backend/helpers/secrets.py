import json
import boto3
from botocore.exceptions import ClientError
from .helpers import is_dev
import os

def get_django_secret_key():
    secret_name = f"{"dev" if is_dev() else "prod"}/chattex/django_secret_key"
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=os.environ.get("REGION")
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
        region_name=os.environ.get("REGION")
    )
    try:
        secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e
    secret = json.loads(secret_value_response['SecretString'])['INVITE_CODE']
    return secret

def get_rds_credentials():
    secret_name = os.environ.get("RDS_SM")
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=os.environ.get("REGION")
    )
    try:
        secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e
    secret = json.loads(secret_value_response['SecretString'])
    return secret
