from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import uuid
from .. import schemas
from ..models import User, Post, Like
from ..security import create_jwt_token

def get_all_posts(user: schemas.User, db: Session) -> list[schemas.PostView]:
    _posts = db.query(Post).order_by(Post.created_at.desc()).all()
    posts = []
    for post in _posts:
        author = db.query(User).filter_by(id=post.user_id).first()
        likes = db.query(Like).filter_by(post_id=post.id).count()
        liked = db.query(Like).filter_by(post_id=post.id, user_id=user.id).first() is not None
        
        _post = schemas.PostView(
            id=post.id,
            content=post.content,
            author=schemas.User.from_orm(author),
            likes=likes,
            liked=liked,
            time=post.time
        )
        posts.append(_post)
    
    return posts

def create_post(user: schemas.User, content: schemas.PostCreate, db: Session) -> schemas.PostView:
    new_post = Post(user_id=user.id, content=content.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    post = schemas.PostView(
        id=new_post.id,
        content=new_post.content,
        author=schemas.User.from_orm(user),
        likes=0,
        liked=False,
        time=new_post.time
    )
    
    return post

def edit_post(user: schemas.User, info: schemas.PostEdit, db: Session) -> schemas.PostView:
    post = db.query(Post).filter_by(id=info.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    post.content = info.content
    db.commit()
    db.refresh(post)
    
    return schemas.PostView(
        id=post.id,
        content=post.content,
        author=schemas.User.from_orm(user),
        likes=db.query(Like).filter_by(post_id=post.id).count(),
        liked=False,
        time=post.time
    )

def delete_post(user: schemas.User, info: schemas.PostAction, db: Session) -> schemas.BaseResponse:
    post = db.query(Post).filter_by(id=info.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    db.delete(post)
    db.commit()
    
    return schemas.BaseResponse(message="Post deleted")

def toggle_like(user: schemas.User, info: schemas.PostAction, db: Session) -> schemas.BaseResponse:
    post = db.query(Post).filter_by(id=info.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if post.user_id == user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't like own post")

    like = db.query(Like).filter_by(post_id=post.id, user_id=user.id).first()
    if like:
        db.delete(like)
        db.commit()
        return schemas.BaseResponse(message="Like removed")
    
    like = Like(post_id=post.id, user_id=user.id)
    db.add(like)
    db.commit()
    
    return schemas.BaseResponse(message="Liked")