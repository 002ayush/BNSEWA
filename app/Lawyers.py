from app import mongo
from bson import ObjectId

class Lawyers:
    def __init__(self, name,about, phone_no, email, city, registration_number,
                 bar_council_name, specialization, available_slots,
                 experience_years, active=False):
        self.name = name
        self.about = about
        self.phone_no = phone_no
        self.email = email
        self.city = city
        self.registration_number = registration_number
        self.bar_council_name = bar_council_name
        self.specialization = specialization
        self.available_slots = available_slots
        self.experience_years = experience_years
        self.active = active

    def to_dict(self):
        return {
            "name": self.name,
            "about": self.about,
            "phone_no": self.phone_no,
            "email": self.email,
            "city": self.city,
            "registration_number": self.registration_number,
            "bar_council_name": self.bar_council_name,
            "specialization": self.specialization,
            "available_slots": self.available_slots,
            "experience_years": self.experience_years,
            "active": self.active
        }

    def save(self):
        existing = mongo.db.lawyers.find_one({"email": self.email})
        if existing:
            return {"error": "Lawyer with this email already exists."}
        
        mongo.db.lawyers.insert_one(self.to_dict())
        return {"message": "Lawyer added successfully"}

    @staticmethod
    def find_all():
        lawyers = mongo.db.lawyers.find({"active": True})
        return [{**lawyer, "_id": str(lawyer["_id"])} for lawyer in lawyers]

    @staticmethod
    def find_by_id(lawyer_id):
        try:
            lawyer = mongo.db.lawyers.find_one({"_id": ObjectId(lawyer_id)})
            if lawyer:
                lawyer["_id"] = str(lawyer["_id"])
                return lawyer
            return {"error": "Lawyer not found"}
        except Exception:
            return {"error": "Invalid ID format"}
