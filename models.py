from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__='users'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    user_id = Column(String)