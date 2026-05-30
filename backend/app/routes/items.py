from flask import Blueprint, request, current_app, jsonify
from ..utils.helpers import get_db, success_response, error_response

items_bp = Blueprint('items', __name__)

@items_bp.route('/debug', methods=['GET'])
def debug_info():
    """Debug endpoint to show DB config and test connection"""
    info = {
        'host': current_app.config.get('MYSQL_HOST'),
        'port': current_app.config.get('MYSQL_PORT'),
        'database': current_app.config.get('MYSQL_DB'),
        'user': current_app.config.get('MYSQL_USER'),
        'ssl': current_app.config.get('MYSQL_SSL', False)
    }
    try:
        conn = get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT 1 as ok')
                res = cursor.fetchone()
        finally:
            conn.close()
        return jsonify({'status': 'ok', 'db_info': info, 'test_query': res}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'db_info': info, 'error': str(e)}), 500

@items_bp.route('/', methods=['GET'])
def get_items():
    category = request.args.get('category')  # movie, music, book
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    offset = (page - 1) * limit

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            if category:
                cursor.execute(
                    "SELECT * FROM items WHERE category = %s LIMIT %s OFFSET %s",
                    (category, limit, offset)
                )
            else:
                cursor.execute("SELECT * FROM items LIMIT %s OFFSET %s", (limit, offset))
            items = cursor.fetchall()
            return success_response(data=items)
    finally:
        conn.close()

@items_bp.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
            item = cursor.fetchone()
            if not item:
                return error_response("Item not found", 404)

            # Fetch category-specific details
            if item['category'] == 'book':
                cursor.execute("SELECT * FROM book_details WHERE item_id = %s", (item_id,))
            elif item['category'] == 'movie':
                cursor.execute("SELECT * FROM movie_details WHERE item_id = %s", (item_id,))
            elif item['category'] == 'music':
                cursor.execute("SELECT * FROM music_details WHERE item_id = %s", (item_id,))
            details = cursor.fetchone()
            item['details'] = details

            # Average rating
            cursor.execute(
                "SELECT AVG(score) as avg_rating, COUNT(*) as total FROM ratings WHERE item_id = %s",
                (item_id,)
            )
            item['rating_info'] = cursor.fetchone()
            return success_response(data=item)
    finally:
        conn.close()
