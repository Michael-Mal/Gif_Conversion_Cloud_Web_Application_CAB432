# This code has been repurposed from the Week 4 JSON Web Token Practical found at 
# https://canvas.qut.edu.au/courses/20367/pages/practical-authentication-and-sessions-in-fastapi-with-json-web-tokens-python?module_item_id=2063599
# , specifically the sample FastAPI app that can be downloaded from https://canvas.qut.edu.au/courses/20367/files/6717519/download

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import datetime
import sys
import os
from datetime import timezone


def get_secret_key():
    import app
    return app.app.secret_key

users = {
    'michael': {
        'password': 'mallett'
    },
    'test_account_1': {
        'password': 'test_password'
    }
}

security = HTTPBearer()

def generate_access_token(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.now(timezone.utc) + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, get_secret_key(), algorithm='HS256')
    return token

def authenticate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials or not credentials.scheme == 'Bearer':
        raise HTTPException(status_code=401, detail='Unauthorised')
    token = credentials.credentials
    try:
        user = jwt.decode(token, get_secret_key(), algorithms=['HS256'])
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token has expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')
    
async def login(request: Request):
    """Login to an account

    Args:
        request (Request): A dictionary containing the username and password to login with.

    Raises:
        HTTPException: If the user does not exist or the password is not correct

    Returns:
        dict: The authorisation token to be used in subsequent requests
    """
    data = await request.json()
    username = data.get('username')
    password = data.get('password')
    user = users.get(username)
    if not user or user['password'] != password:
        raise HTTPException(status_code=401, detail='Unauthorised')
    token = generate_access_token(username)
    return { 'authToken': token }