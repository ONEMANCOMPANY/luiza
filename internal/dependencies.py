import httpx
import base64
import smtplib
import os
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from fastapi import FastAPI
from datetime import datetime, timedelta
from typing import Union, List
from fastapi import Depends, FastAPI, HTTPException, status, WebSocket
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing_extensions import Annotated
from users.schemas import Token, TokenData
from users.models import UserModel


app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
state = secrets.token_urlsafe(16)
blacklisted_tokens = []
password_reset_tokens = {}
connected_websockets = set()
websocket_connections: List[WebSocket] = []
URL = f'http://localhost:8000' if not "production" in os.environ else f'http://193.203.174.195:8000'

# Configuração do servidor SMTP
SMTP_SERVER = "smtps.uol.com.br"
SMTP_PORT = 587
SMTP_USERNAME = "notificacao@metasolucoesambientais.com.br"
SMTP_PASSWORD = "Meta33650913@"

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(email: str, password: str):
    # about.wendrew@gmail.com 
    # sunsix123
    user = UserModel.get_password_email(email)
    if not user:
        return False
    if not verify_password(password, user[0]):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    print(data)
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        exps: int = payload.get("exp")

        if username is None:
            raise credentials_exception
        
        if token in blacklisted_tokens:
            raise credentials_exception
        
        token_data = TokenData(username=username, expires=exps)
    except JWTError:
        raise credentials_exception
    
    user = UserModel.get_user_email(email=token_data.username)
    
    if user is None:
        raise credentials_exception
    
    if exps is None:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: Annotated[UserModel, Depends(get_current_user)]):
    if not current_user:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
