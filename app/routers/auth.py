from app import database, schemas
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..repositories import auth
from .. import schemas

from ..security import get_user

router = APIRouter(
    prefix = "",
    tags = ['auth']
)

get_db = database.get_db

@router.post("/register", response_model=schemas.BaseResponse, status_code=status.HTTP_201_CREATED)
def register(request: schemas.RegistrationRequest, db: Session = Depends(get_db)):
    return auth.register(request, db)

@router.post("/login", response_model=schemas.LoginResponse)
def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    return auth.login(request, db)

@router.get("/send-verification", response_model=schemas.BaseResponse)
def send_verification(user: schemas.User = Depends(get_user), db: Session = Depends(get_db)):
    return auth.send_verification(user, db)

@router.get("/verify/{code}", response_model=schemas.BaseResponse)
def verify(code: str, db: Session = Depends(get_db)):
    return auth.verify(code, db)

@router.get("/current-user", response_model=schemas.User)
def current_user(user: schemas.User = Depends(get_user)):
    return user