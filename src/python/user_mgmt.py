# File: user_mgmt.py

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import User, Base
"""
Module: User Management

Objective: 
    To manage parent and child user classes including user creation, modification, and authentication.

Dependencies: 
    SQLite database

Imports Needed: 
    SQLAlchemy

Outputs: 
    User objects with associated metadata
    Authentication tokens or sessions (to be implemented later)
"""

Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)  # Please hash this in production
    user_type = Column(String)  # 'Parent' or 'Child'

# Initialize the SQLite database
engine = create_engine('sqlite:///users.db')

# Create the table
Base.metadata.create_all(engine)

# Create a Session class
Session = sessionmaker(bind=engine)

# Initialize a session
session = Session()

def create_user(username, password, user_type):
    new_user = User(username=username, password=password, user_type=user_type)
    session.add(new_user)
    session.commit()

def authenticate_user(username, password):
    user = session.query(User).filter_by(username=username, password=password).first()
    return user is not None

def get_user_info(username):
    user = session.query(User).filter_by(username=username).first()
    return {
        "id": user.id,
        "username": user.username,
        "user_type": user.user_type
    } if user else None

def delete_user(username, password):
    if authenticate_user(username, password) and get_user_info(username)['user_type'] == 'Parent':
        user = session.query(User).filter_by(username=username).first()
        session.delete(user)
        session.commit()
        return True
    return False

# Interactive prompt
if __name__ == "__main__":
    while True:
        print("1: Select Active User")
        print("2: Create User")
        print("3: Delete User")
        print("4: Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if authenticate_user(username, password):
                print(f"Welcome {username}!")
                # Do stuff as the authenticated user
            else:
                print("Invalid credentials.")

        elif choice == '2':
            username = input("Enter new username: ")
            password = input("Enter new password: ")
            user_type = input("Enter user type (Parent/Child): ")
            create_user(username, password, user_type)
            print(f"User {username} created.")

        elif choice == '3':
            username = input("Enter Parent username: ")
            password = input("Enter Parent password: ")
            if delete_user(username, password):
                print(f"User {username} deleted.")
            else:
                print("Could not delete user. Only a Parent user can delete.")

        elif choice == '4':
            break

        else:
            print("Invalid option.")
