from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .. import db
from ..models import User

auth_bp = Blueprint('auth', __name__)

CORS(auth_bp)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No input data provided"}), 400
            
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return jsonify({"error": "Missing required fields"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 400

        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({"message": "User created successfully", "user_id": user.id}), 201
        
    return jsonify({"message": "Signup endpoint"}), 200


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"error": "Invalid email or password"}), 401

    login_user(user)
    
    # Create JWT token with the user ID as identity - convert to string
    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,  
        "user_id": user.id,
        "username": user.username
    }), 200


@auth_bp.route('/logout')
@jwt_required()
def logout():
    # With JWT, client should discard token, server-side we don't need to do anything
    # but we keep the endpoint for API consistency
    return jsonify({"message": "Logged out successfully"}), 200
