from botocore.exceptions import ClientError
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient
from fastapi import HTTPException, Depends, Header, Form
from gma_code.dao.secrets_loader import get_secret
from gma_code.dao.parameter_store import get_parameter
from pydantic import BaseModel
import hmac, hashlib, base64, jwt
import boto3


# --------------------
# Config
# --------------------


client_id = "6uc0hq56f73gliee8er2u0g1et"
client_secret = get_secret("A2_Group11-CognitoSecret")["COGNITO-SECRET"]

# --------------------
# SecretHash Helper
# --------------------

def secretHash(clientId, clientSecret, username):
    message = bytes(username + clientId, 'utf-8')
    key = bytes(clientSecret, 'utf-8')
    return base64.b64encode(hmac.new(key, message, digestmod=hashlib.sha256).digest()).decode()

# --------------------
# ensures inputs are in JSON
# --------------------

class SignUpIn(BaseModel):
    username: str
    email: str
    password: str

class ConfirmIn(BaseModel):
    username: str
    code: str

class LoginIn(BaseModel):
    username: str
    password: str

# --------------------
# Signup Helper
# --------------------


def signup(username: str = Form(...), 
           email: str = Form(...), 
           password: str = Form(...)):
    client = boto3.client("cognito-idp", region_name=get_parameter("aws_region"))
    try:
        response = client.sign_up(
            ClientId=client_id,
            Username=username,
            Password=password,
            SecretHash=secretHash(client_id, client_secret, username),
            UserAttributes=[
                {"Name": "email", "Value": email}
            ],
        )
        return response
    except ClientError as e:
        print(f"Error during sign-up: {e}")
        return None



# --------------------
# Confirmation Helper
# --------------------


def confirm_user(username: str = Form(...), 
                 code: str = Form(...)):
    client = boto3.client("cognito-idp", region_name=get_parameter("aws_region"))
    try:
        return client.confirm_sign_up(
            ClientId=client_id,
            Username=username,
            ConfirmationCode=code,
            SecretHash=secretHash(client_id, client_secret, username),
        )
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response["Error"]["Message"])


# --------------------
# Authenticate helper
# --------------------


def authenticate(username: str = Form(...), 
                 password: str = Form(...)):
    client = boto3.client("cognito-idp", region_name=get_parameter("aws_region"))
    try:
        response = client.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password,
                "SECRET_HASH": secretHash(client_id, client_secret, username),
            },
            ClientId=client_id,
        )
        tokens = response["AuthenticationResult"]
        return tokens
    except Exception as e:
        print(f"Error during authenticate: {e}")
        return None

# --------------------
# authentication token
# --------------------

JWKS_URL = f"https://cognito-idp.ap-southeast-2.amazonaws.com/ap-southeast-2_I0recdlvf/.well-known/jwks.json"
_jwkclient = PyJWKClient(JWKS_URL)
_security = HTTPBearer()

def _decode_cognito_jwt(token: str):
    signing_key = _jwkclient.get_signing_key_from_jwt(token).key

    decoded = jwt.decode(
        token,
        signing_key,
        algorithms=["RS256"],
        options={"verify_exp": True, "verify_aud": False},
    )
    token_use = decoded.get("token_use")
    if token_use not in ("id", "access"):
        raise HTTPException(status_code=401, detail="Invalid token_use")
        # For ID tokens, ensure this token was intended for your app client (aud = client_id)
    if token_use == "id" and decoded.get("aud") != client_id:
        raise HTTPException(status_code=401, detail="Wrong audience for ID token")
        # Pull a sensible username:
    uname = decoded.get("cognito:username") or decoded.get("username") or decoded.get("sub")
    return {"username": uname, "claims": decoded, "token_use": token_use}


def authenticate_token(credentials: HTTPAuthorizationCredentials = Depends(_security)):
    if not credentials or credentials.scheme != "Bearer":
        raise HTTPException(status_code=401, detail="Unauthorised")
    token = credentials.credentials
    try:
        return _decode_cognito_jwt(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")





