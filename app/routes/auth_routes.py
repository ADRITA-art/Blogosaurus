from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_cors import CORS
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
            
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 400
            
        # Create new user
        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({"message": "User created successfully", "user_id": user.id}), 201
        
    return jsonify({"message": "Signup endpoint"}), 200


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No input data provided"}), 400
            
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"error": "Missing email or password"}), 400
            
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return jsonify({
                "message": "Login successful",
                "user_id": user.id,
                "username": user.username
            }), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
            
    return jsonify({"message": "Login endpoint"}), 200


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200
