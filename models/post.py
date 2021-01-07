from werkzeug.exceptions import NotFound
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from models.database import db
from sqlalchemy.orm import relationship

class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)

    posts = relationship("Post", back_populates="user")

class Post(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    title = Column(String(50), nullable=False)
    text = Column(Text, nullable=False)
    is_published = Column(Boolean, nullable=False, default=False)
    deleted = Column(Boolean, nullable=False, default=False, server_default="0")

    user = relationship(User, back_populates="posts")

    @classmethod
    def get_post_by_id(cls, post_id, deleted=False):
        post = cls.query.filter_by(deleted=deleted, id=post_id).one_or_none()
        if post is None:
            raise NotFound(f"Product #{post_id} not found!")
        return post
