from urllib import request

import jwt
from datetime import datetime, timezone, timedelta

from users.models import User
from main import settings

def generate_access_token(username):
    payload = {
        'username' : username,
        'exp' : datetime.utcnow() + timedelta(minutes=5),
        'iat' : datetime.utcnow(),
        'type' : 'access'
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

def generate_refresh_token(username):
    payload = {
        'username' : username,
        'exp' : datetime.utcnow() + timedelta(minutes=60),
        'iat' : datetime.utcnow(),
        'type' : 'refresh'
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        exp = payload.get('exp')
        print(f"exp = {exp}")
        if exp is None:
            raise jwt.InvalidTokenError("Token has no expiration")
        if datetime.now(timezone.utc).timestamp() > exp:
            raise jwt.ExpiredSignatureError("Token has expired")

        return payload

    except jwt.ExpiredSignatureError:
        raise Exception("Access token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid access token")
