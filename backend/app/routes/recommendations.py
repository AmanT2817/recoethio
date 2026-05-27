from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils.helpers import get_db, success_response, error_response
from ..ml.hybrid import get_hybrid_recommendations

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/', methods=['GET'])
@jwt_required()
def get_recommendations():
    user_id = int(get_jwt_identity())
    category = request.args.get('category')  # optional filter

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as cnt FROM ratings WHERE user_id = %s", (user_id,))
            count = cursor.fetchone()['cnt']

        if count < 5:
            # Cold start: return popular items
            with conn.cursor() as cursor:
                query = """SELECT i.*, AVG(r.score) as avg_score, COUNT(r.id) as rating_count
                           FROM items i LEFT JOIN ratings r ON i.id = r.item_id"""
                if category:
                    query += " WHERE i.category = %s"
                    query += " GROUP BY i.id ORDER BY avg_score DESC, rating_count DESC LIMIT 20"
                    cursor.execute(query, (category,))
                else:
                    query += " GROUP BY i.id ORDER BY avg_score DESC, rating_count DESC LIMIT 20"
                    cursor.execute(query)
                items = cursor.fetchall()
                return success_response(data={"type": "popular", "items": items})

        recs = get_hybrid_recommendations(user_id, category, conn)
        return success_response(data={"type": "personalized", "items": recs})
    finally:
        conn.close()
