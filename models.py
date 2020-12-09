from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, Boolean, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

engine = create_engine("sqlite:///my_post.db")
Base = declarative_base(bind=engine)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)

    posts = relationship("Post", back_populates="user")

    def __str__(self):
        return str(self.username)

    def __repr__(self):
        return str(self)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    title = Column(String(50), nullable=False)
    text = Column(Text, nullable=False)
    is_published = Column(Boolean, nullable=False, default=False)
    date = Column(Date, nullable=False)

    user = relationship(User, back_populates="posts")
    tags = relationship("Tag", back_populates="posts")

    def __str__(self):
        return str(self.title)

    def __repr__(self):
        return str(self)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(16), nullable=False, unique=True)

    posts = relationship("Post", back_populates="tags")

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self)

