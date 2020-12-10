from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, Boolean, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

engine = create_engine("sqlite:///my_post.db")
metadata = MetaData(bind=engine)
Base = declarative_base(bind=engine)

posts_tags_m2m_table = Table(
    "posts_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")

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

    user = relationship(User, back_populates="posts")
    tags = relationship("Tag", secondary=posts_tags_m2m_table, back_populates="posts")
    comments = relationship("Comment", back_populates="posts")

    def __str__(self):
        return str(self.title)

    def __repr__(self):
        return str(self)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(16), nullable=False, unique=True)

    posts = relationship(Post, secondary=posts_tags_m2m_table, back_populates="tags")

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self)


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    id_post = Column(Integer, ForeignKey(Post.id),nullable=False)
    text = Column(Text, nullable=False)
    parent_comment = Column(Integer, nullable=True)

    user = relationship(User, back_populates="comments")
    posts = relationship(Post, back_populates="comments")

    def __str__(self):
        return str(self.text)

    def __repr__(self):
        return str(self)

def create_users_and_posts_and_tags_and_comments():
    session = Session()

    user1 = User(username="Anna")
    session.add(user1)
    user2 = User(username="Mark")
    session.add(user2)

    session.flush()

    post1 = Post(user_id=user1.id, title="Strengthening exercises",
                 text="Strengthening activities focus on building up or maintaining strength in your major muscle"
                      " groups – for example, your arms and legs. Doing exercises to improve strength is important"
                      " throughout life. ")
    post2 = Post(user_id=user1.id, title="Aerobic exercise",
                 text="Aerobic exercise is any type of continuous activity that works your heart, lungs and muscles. "
                      "Examples include brisk walking, cycling, running, swimming, dancing and football.")
    session.add(post1)
    session.add(post2)

    tag_news_1 = Tag(name="exercise")
    tag_news_2 = Tag(name="aerobic")
    tag_news_3 = Tag(name="strengthening")

    session.add(tag_news_1)
    session.add(tag_news_2)
    session.add(tag_news_3)

    session.flush()

    post1.tags.extend((tag_news_1, tag_news_3))
    post2.tags.extend((tag_news_1, tag_news_2))

    comment1 = Comment(user_id=user2.id, id_post=post1.id,
                       text='Swimming is a great form of exercise for people of all ages and abilities.')

    comment2 = Comment(user_id=user1.id, id_post=post1.id,
                       text=' It’s also a great choice if you have any problems with your joints, such as arthritis.',
                       parent_comment=comment1.id)

    session.add(comment1)
    session.add(comment2)

    session.commit()

    session.close()


if __name__ == '__main__':
    Base.metadata.create_all()
    create_users_and_posts_and_tags_and_comments()

    posts_table = Table(
        "posts",
        metadata,
        autoload=True
    )

    posts111 = posts_table.get(Post.user_id == 1)

    print(posts111.user_id)

    # for c in posts_table.
    #     print(f"Column {c.name!r}:", repr(c))
