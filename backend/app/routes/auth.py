from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from ..utils.helpers import get_db, success_response, error_response

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return error_response("All fields are required", 400)

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                return error_response("Email already registered", 409)
            hashed = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, hashed)
            )
            conn.commit()
            return success_response(message="User registered successfully", status=201)
    finally:
        conn.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if not user or not check_password_hash(user['password_hash'], password):
                return error_response("Invalid credentials", 401)
            token = create_access_token(identity=str(user['id']))
            return success_response(data={"token": token, "user": {
                "id": user['id'], "username": user['username'],
                "email": user['email'], "role": user['role']
            }})
    finally:
        conn.close()

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, username, email, role, created_at FROM users WHERE id = %s", (user_id,)
            )
            user = cursor.fetchone()
            return success_response(data=user)
    finally:
        conn.close()


@auth_bp.route('/onboarding', methods=['POST'])
@jwt_required()
def onboarding():
    user_id = get_jwt_identity()
    data = request.get_json()
    preferences = data.get('preferences', [])

    if not preferences or len(preferences) < 3:
        return error_response("Please select at least 3 preferences", 400)

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            # Upsert preferences record
            cursor.execute("SELECT id FROM preferences WHERE user_id = %s", (user_id,))
            existing = cursor.fetchone()
            prefs_str = ','.join(preferences)
            if existing:
                cursor.execute(
                    "UPDATE preferences SET fav_genres = %s WHERE user_id = %s",
                    (prefs_str, user_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO preferences (user_id, fav_genres) VALUES (%s, %s)",
                    (user_id, prefs_str)
                )
            # Mark user as onboarded
            cursor.execute(
                "UPDATE users SET bio = 'onboarded' WHERE id = %s", (user_id,)
            )
            conn.commit()
            return success_response(message="Preferences saved", status=200)
    finally:
        conn.close()
