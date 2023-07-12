from typing import List, Optional
from pydantic import BaseModel, EmailStr
import uuid
import enum
import datetime

class BaseResponse(BaseModel):
    message: str

# Auth schemas
class RegistrationRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    token: str
    verified: bool

class UserUnverified(BaseModel):
    id: uuid.UUID
    name: str

class User(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    is_verified: bool

    class Config:
        orm_mode = True

# Post schemas
class PostView(BaseModel):
    id: uuid.UUID
    content: str
    author: User
    likes: int
    liked: bool
    time: datetime.datetime

class PostCreate(BaseModel):
    content: str

class PostEdit(BaseModel):
    id: uuid.UUID
    content: str

class PostAction(BaseModel):
    id: uuid.UUID