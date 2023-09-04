# File: chore_mgmt.py

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from models import Chore, User, Base

"""
Module: Chore Management

Objective: 
    To manage chores including chore creation, modification, and completion tracking.

Dependencies: 
    SQLite database

Imports Needed: 
    SQLAlchemy

Outputs: 
    Chore objects with associated metadata
    Status updates (e.g., chore marked as complete)
"""

Base = declarative_base()

# Define the Chore model
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

# Initialize the SQLite database
engine = create_engine('sqlite:///chores.db')

# Create the table
Base.metadata.create_all(engine)

# Create a Session class
Session = sessionmaker(bind=engine)

# Initialize a session
session = Session()

def add_chore(name, dollar_value, user_id):
    new_chore = Chore(name=name, dollar_value=dollar_value, user_id=user_id)
    session.add(new_chore)
    session.commit()

def mark_complete(chore_id):
    chore = session.query(Chore).filter_by(id=chore_id).first()
    chore.is_complete = True
    session.commit()

def list_chores(user_id):
    chores = session.query(Chore).filter_by(user_id=user_id).all()
    return [(chore.id, chore.name, chore.dollar_value, chore.is_complete) for chore in chores]

# Interactive prompt
if __name__ == "__main__":
    while True:
        print("1: Add Chore")
        print("2: Mark Chore as Complete")
        print("3: List Chores")
        print("4: Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Enter chore name: ")
            dollar_value = int(input("Enter dollar value: "))
            user_id = int(input("Enter user ID: "))
            add_chore(name, dollar_value, user_id)
            print(f"Chore {name} added.")

        elif choice == '2':
            chore_id = int(input("Enter chore ID to mark as complete: "))
            mark_complete(chore_id)
            print(f"Chore {chore_id} marked as complete.")

        elif choice == '3':
            user_id = int(input("Enter user ID: "))
            chores = list_chores(user_id)
            print("ID | Name | Dollar Value | Is Complete")
            for id, name, dollar_value, is_complete in chores:
                print(f"{id} | {name} | {dollar_value} | {is_complete}")

        elif choice == '4':
            break

        else:
            print("Invalid option.")

