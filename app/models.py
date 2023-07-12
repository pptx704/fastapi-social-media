from app.database import Base
from sqlalchemy.sql import func
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Index
from secrets import token_urlsafe

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String(60), nullable=False)
    is_verified = Column(Boolean, default=False)

    posts = relationship("Post", backref="user")
    likes = relationship("Like", backref="user")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, is_active={self.is_verified}>"
    
class Code(Base):
    __tablename__ = 'auth_codes'

    code = Column(String(64), primary_key=True, index=True, default=lambda: token_urlsafe(48))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    usable = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"user_id={self.user_id}, code={self.code[:10]}, usable={self.usable}>"
    

class Post(Base):
    __tablename__ = 'posts'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    content = Column(String(512), nullable=False)

    likes = relationship("Like", backref="post")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    @property
    def time(self):
        if self.updated_at:
            return self.updated_at
        return self.created_at

    def __repr__(self):
        return f"<Post(id={self.id}, content={self.content[:10]}>"
    
class Like(Base):
    __tablename__ = 'post_likes'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey('posts.id', ondelete="CASCADE"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'post_id'),
    )

    def __repr__(self):
        return f"<Like(user_id={self.user_id}, post_id={self.post_id}>"