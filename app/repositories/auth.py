from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas
from ..models import User, Code
from ..security import get_password_hash, verify_password, create_jwt_token
from datetime import datetime, timedelta

from ..utils import verify_email

def register(request: schemas.RegistrationRequest, db: Session) -> schemas.BaseResponse:
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    if request.password != request.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    
    verify, message = verify_email(request.email)
    if not verify:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    user = User(
        name = request.name,
        email = request.email,
        password_hash = get_password_hash(request.password),
    )

    db.add(user)
    db.commit()

    return schemas.BaseResponse(message="Registration successful")

def login(request: schemas.LoginRequest, db: Session):
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    
    token = create_jwt_token({"user_id": str(user.id)})

    return schemas.LoginResponse(
        token=token, 
        verified=user.is_verified
    )

def send_verification(user: schemas.User, db: Session):
    code_obj = Code(
        user_id=user.id
    )

    db.add(code_obj)
    db.commit()

    # returning the code here but originally a link will be formed and sent to the user's email
    return schemas.BaseResponse(message=f"{code_obj.code}")

def verify(code: str, db: Session):
    code_obj = db.query(Code).filter_by(code=code).first()
    if not code_obj or not code_obj.usable:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid code")
    
    if code_obj.created_at + timedelta(minutes=30) < datetime.now():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Code expired")

    user = db.query(User).filter_by(id=code_obj.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user.is_verified = True
    code_obj.usable = False

    db.commit()

    return schemas.BaseResponse(message="Verification successful")