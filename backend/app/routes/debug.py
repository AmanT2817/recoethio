from flask import Blueprint, current_app, jsonify
from ..utils.helpers import get_db

debug_bp = Blueprint('debug', __name__)


@debug_bp.route('/db', methods=['GET'])
def db_debug():
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
