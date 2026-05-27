from flask import Blueprint, request
from ..utils.helpers import get_db, success_response, error_response

search_bp = Blueprint('search', __name__)

@search_bp.route('/', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    category = request.args.get('category')
    is_ethiopian = request.args.get('ethiopian')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    offset = (page - 1) * limit

    if not query:
        return error_response("Search query is required", 400)

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            sql = """SELECT i.* FROM items i
                     WHERE (i.title LIKE %s OR i.description LIKE %s)"""
            params = [f"%{query}%", f"%{query}%"]

            if category:
                sql += " AND i.category = %s"
                params.append(category)
            if is_ethiopian:
                sql += " AND i.is_ethiopian = 1"

            sql += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])

            cursor.execute(sql, params)
            return success_response(data=cursor.fetchall())
    finally:
        conn.close()
