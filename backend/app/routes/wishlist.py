from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils.helpers import get_db, success_response, error_response

wishlist_bp = Blueprint('wishlist', __name__)

@wishlist_bp.route('/', methods=['GET'])
@jwt_required()
def get_wishlist():
    user_id = get_jwt_identity()
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT w.*, i.title, i.category, i.cover_image
                   FROM wishlist w JOIN items i ON w.item_id = i.id
                   WHERE w.user_id = %s ORDER BY w.added_at DESC""",
                (user_id,)
            )
            return success_response(data=cursor.fetchall())
    finally:
        conn.close()

@wishlist_bp.route('/', methods=['POST'])
@jwt_required()
def add_to_wishlist():
    user_id = get_jwt_identity()
    item_id = request.get_json().get('item_id')
    if not item_id:
        return error_response("item_id is required", 400)

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT IGNORE INTO wishlist (user_id, item_id) VALUES (%s, %s)",
                (user_id, item_id)
            )
            conn.commit()
            return success_response(message="Added to wishlist", status=201)
    finally:
        conn.close()

@wishlist_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_wishlist(item_id):
    user_id = get_jwt_identity()
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM wishlist WHERE user_id = %s AND item_id = %s",
                (user_id, item_id)
            )
            conn.commit()
            return success_response(message="Removed from wishlist")
    finally:
        conn.close()
