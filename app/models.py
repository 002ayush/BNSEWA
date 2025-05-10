from app import mongo
from datetime import datetime

class User:
    def __init__(self, username, email, password, profile_picture=None):
        self.username = username
        self.email = email
        self.password = password
        self.profile_picture = profile_picture
        self.created_at = datetime.utcnow()

    def save(self):
        user_data = {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "profile_picture": self.profile_picture,
            "created_at": self.created_at
        }
        mongo.db.users.insert_one(user_data)  # Insert into MongoDB users collection

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({"email": email})  # Find user by email

    @staticmethod
    def find_by_id(user_id):
        return mongo.db.users.find_one({"_id": user_id})  # Find user by ID
