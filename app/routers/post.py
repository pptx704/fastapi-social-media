from fastapi import APIRouter, Depends, HTTPException, status
from app import database, schemas
from sqlalchemy.orm import Session
import uuid
from ..repositories import auth, post
from ..security import get_user, get_user_strict

router = APIRouter(
    prefix = "/post",
    tags = ['posts']
)

get_db = database.get_db

@router.get("/all", response_model=list[schemas.PostView])
def get_all_posts(user: schemas.User = Depends(get_user), db: Session = Depends(get_db)):
    return post.get_all_posts(user, db)

@router.post("/create", response_model=schemas.PostView, status_code=status.HTTP_201_CREATED)
def create_post(content: schemas.PostCreate, user: schemas.User = Depends(get_user_strict), db: Session = Depends(get_db)):
    return post.create_post(user, content, db)

@router.post("/edit", response_model=schemas.PostView)
def edit_post(info: schemas.PostEdit, user: schemas.User = Depends(get_user_strict), db: Session = Depends(get_db)):
    return post.edit_post(user, info, db)

@router.post("/delete", response_model=schemas.BaseResponse)
def delete_post(info: schemas.PostAction, user: schemas.User = Depends(get_user_strict), db: Session = Depends(get_db)):
    return post.delete_post(user, info, db)

@router.post("/like", response_model=schemas.BaseResponse, name="Like or unlike post")
def like_post(info: schemas.PostAction, user: schemas.User = Depends(get_user_strict), db: Session = Depends(get_db)):
    return post.toggle_like(user, info, db)