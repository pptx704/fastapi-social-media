import os
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from app.models import User

from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .database import get_db
from .models import User
from .const import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

from . import schemas

pwd_context = CryptContext(schemes=["bcrypt"])

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt_token(data: dict) -> str:
    _ed = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    iat = datetime.utcnow()
    exp = datetime.utcnow() + _ed
    token_payload = data
    token_payload.update({"iat": iat, "exp": exp})

    token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)

    return token

def get_user_from_token(token: str) -> schemas.User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user_id = payload.get("user_id")
    
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    with next(get_db()) as db:
        user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return schemas.User.from_orm(user)

def get_user(authorization: HTTPAuthorizationCredentials = Security(HTTPBearer())) -> schemas.User:
    if authorization.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    
    token = authorization.credentials
    return get_user_from_token(token)

def get_user_strict(authorization: HTTPAuthorizationCredentials = Security(HTTPBearer())) -> schemas.User:
    user = get_user(authorization)
    if not user.is_verified:
        raise HTTPException(status_code=401, detail="User not verified")
    
    return user