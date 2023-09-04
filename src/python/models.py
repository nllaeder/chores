# models.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    password = Column(String)
    user_type = Column(String)  # Parent or Child

class Chore(Base):
    __tablename__ = 'chores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    dollar_value = Column(Integer)
    is_complete = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="chores")

# Add a 'chores' attribute to the User model to create a one-to-many relationship
User.chores = relationship("Chore", order_by=Chore.id, back_populates="user")
