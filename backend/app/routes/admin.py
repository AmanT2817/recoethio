from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils.helpers import get_db, success_response, error_response

admin_bp = Blueprint('admin', __name__)

def require_admin(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        return user and user['role'] == 'admin'

@admin_bp.route('/items', methods=['POST'])
@jwt_required()
def add_item():
    user_id = get_jwt_identity()
    conn = get_db()
    try:
        if not require_admin(user_id, conn):
            return error_response("Admin access required", 403)
        data = request.get_json()
        with conn.cursor() as cursor:
            cursor.execute(
                """INSERT INTO items (title, description, category, genre, release_year,
                   language, cover_image, is_ethiopian)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (data.get('title'), data.get('description'), data.get('category'),
                 data.get('genre'), data.get('release_year'), data.get('language'),
                 data.get('cover_image'), data.get('is_ethiopian', False))
            )
            conn.commit()
            return success_response(message="Item added", status=201)
    finally:
        conn.close()

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    user_id = get_jwt_identity()
    conn = get_db()
    try:
        if not require_admin(user_id, conn):
            return error_response("Admin access required", 403)
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, username, email, role, created_at FROM users")
            return success_response(data=cursor.fetchall())
    finally:
        conn.close()

@admin_bp.route('/users/<int:target_id>', methods=['DELETE'])
@jwt_required()
def delete_user(target_id):
    user_id = get_jwt_identity()
    conn = get_db()
    try:
        if not require_admin(user_id, conn):
            return error_response("Admin access required", 403)
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s", (target_id,))
            conn.commit()
            return success_response(message="User deleted")
    finally:
        conn.close()

@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
def stats():
    user_id = get_jwt_identity()
    conn = get_db()
    try:
        if not require_admin(user_id, conn):
            return error_response("Admin access required", 403)
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as total_users FROM users")
            users = cursor.fetchone()
            cursor.execute("SELECT category, COUNT(*) as count FROM items GROUP BY category")
            items = cursor.fetchall()
            cursor.execute("SELECT COUNT(*) as total_ratings FROM ratings")
            ratings = cursor.fetchone()
            return success_response(data={"users": users, "items": items, "ratings": ratings})
    finally:
        conn.close()
