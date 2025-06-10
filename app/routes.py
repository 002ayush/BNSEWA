# app/routes.py
from flask import Blueprint, request, jsonify
from app import mongo, bcrypt
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.userProfile import UserProfile
from flask import Blueprint
from app.Lawyers import Lawyers

import pickle

routes = Blueprint('routes', __name__)
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('encoders.pkl', 'rb') as f:
    encoders = pickle.load(f)

# Signup route
@routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({'msg': 'Missing fields'}), 400

    # Hash the password
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    # Check if the email already exists
    if User.find_by_email(data['email']):
        return jsonify({'msg': 'Email already in use'}), 400

    # Create a new user instance and save to MongoDB
    user = User(username=data['username'], email=data['email'], password=hashed_pw)
    user.save()
    
    return jsonify({'msg': 'User registered successfully'}), 201

# Login route
@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_data = User.find_by_email(data['email'])
    
    if user_data and bcrypt.check_password_hash(user_data['password'], data['password']):
        access_token = create_access_token(identity=str(user_data['_id']))
        return jsonify({'token': access_token, 'username': user_data['username']}), 200
    
    return jsonify({'msg': 'Invalid credentials'}), 401

# Profile route - get user profile after authentication

@routes.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()

    # Fetch profile from 'profiles' collection using the UserProfile model
    profile = UserProfile.get_by_user_id(user_id)

    if not profile:
        return jsonify({'msg': 'Profile not found'}), 404

    # Return profile information
    return jsonify({
        'full_name': profile.get('full_name'),
        'dob': profile.get('dob'),
        'gender': profile.get('gender'),
        'phone_no': profile.get('phone_no'),
        'email': profile.get('email'),
        'address': profile.get('address'),
        'aadhaar_number': profile.get('aadhaar_number'),
        'pan_number': profile.get('pan_number'),
        'favourite_languages': profile.get('favourite_languages'),
        'emergency_number': profile.get('emergency_number')
    }), 200

@routes.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()

    # Get the updated data from the request
    data = request.get_json()

    # Ensure the profile is created or updated
    profile = UserProfile(
        user_id=user_id,
        full_name=data.get('full_name'),
        dob=data.get('dob'),
        gender=data.get('gender'),
        phone_no=data.get('phone_no'),
        email=data.get('email'),
        address=data.get('address'),
        aadhaar_number=data.get('aadhaar_number'),
        pan_number=data.get('pan_number'),
        favourite_languages=data.get('favourite_languages'),
        emergency_number=data.get('emergency_number')
    )

    # Save or update the profile
    profile.save_or_update()

    return jsonify({'msg': 'Profile updated successfully'}), 200


@routes.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        offense_text = data.get('offense')

        if not offense_text:
            return jsonify({'error': "Missing 'offense' in request"}), 400

        # Transform and predict
        X_input = vectorizer.transform([offense_text])
        prediction = model.predict(X_input)[0]

        # Decode predictions
        result = {
            col: encoders[col].inverse_transform([pred])[0]
            for col, pred in zip(encoders.keys(), prediction)
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@routes.route('/lawyers', methods=['POST'])
def add_lawyer():
    data = request.json
    lawyer = Lawyers(**data)
    result = lawyer.save()
    return jsonify(result)

@routes.route('/lawyers', methods=['GET'])
def get_all_lawyers():
    return jsonify(Lawyers.find_all())

@routes.route('/lawyers/<lawyer_id>', methods=['GET'])
def get_lawyer(lawyer_id):
    return jsonify(Lawyers.find_by_id(lawyer_id))
