from app import mongo
from bson import ObjectId

class UserProfile:
    def __init__(self, user_id, full_name, dob, gender, phone_no, email,
                 address, aadhaar_number, pan_number, favourite_languages, emergency_number):
        self.user_id = ObjectId(user_id)
        self.full_name = full_name
        self.dob = dob
        self.gender = gender
        self.phone_no = phone_no
        self.email = email
        self.address = address
        self.aadhaar_number = aadhaar_number
        self.pan_number = pan_number
        self.favourite_languages = favourite_languages  # e.g., "English, Hindi"
        self.emergency_number = emergency_number

    def save_or_update(self):
        profile_data = {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "dob": self.dob,
            "gender": self.gender,
            "phone_no": self.phone_no,
            "email": self.email,
            "address": self.address,
            "aadhaar_number": self.aadhaar_number,
            "pan_number": self.pan_number,
            "favourite_languages": self.favourite_languages,
            "emergency_number": self.emergency_number
        }

        existing = mongo.db.profiles.find_one({"user_id": self.user_id})
        if existing:
            mongo.db.profiles.update_one({"user_id": self.user_id}, {"$set": profile_data})
        else:
            mongo.db.profiles.insert_one(profile_data)

    @staticmethod
    def get_by_user_id(user_id):
        return mongo.db.profiles.find_one({"user_id": ObjectId(user_id)})
