from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, Boolean, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

engine = create_engine("sqlite:///my_post.db")
Base = declarative_base(bind=engine)

if __name__ == '__main__':
    Base.metadata.create_all()
