from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils.helpers import get_db, success_response, error_response

ratings_bp = Blueprint('ratings', __name__)

@ratings_bp.route('/', methods=['POST'])
@jwt_required()
def rate_item():
    user_id = get_jwt_identity()
    data = request.get_json()
    item_id = data.get('item_id')
    score = data.get('score')
    review = data.get('review', '')

    if not item_id or score is None or not (1 <= int(score) <= 5):
        return error_response("item_id and score (1-5) are required", 400)

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            # Upsert rating
            cursor.execute(
                """INSERT INTO ratings (user_id, item_id, score, review)
                   VALUES (%s, %s, %s, %s)
                   ON DUPLICATE KEY UPDATE score = %s, review = %s, updated_at = NOW()""",
                (user_id, item_id, score, review, score, review)
            )
            conn.commit()
            return success_response(message="Rating saved", status=201)
    finally:
        conn.close()

@ratings_bp.route('/my', methods=['GET'])
@jwt_required()
def my_ratings():
    user_id = get_jwt_identity()
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT r.*, i.title, i.category FROM ratings r
                   JOIN items i ON r.item_id = i.id
                   WHERE r.user_id = %s ORDER BY r.created_at DESC""",
                (user_id,)
            )
            return success_response(data=cursor.fetchall())
    finally:
        conn.close()
