from flask import Blueprint, request
import requests as http_requests
import os
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


@admin_bp.route('/seed-tmdb', methods=['POST'])
def seed_tmdb():
    """Fetch popular movies from TMDB and insert into DB. No auth needed for setup."""
    tmdb_key = os.environ.get('TMDB_API_KEY', '')
    if not tmdb_key:
        return error_response("TMDB_API_KEY not set", 500)

    movies = []
    for page in range(1, 4):  # 3 pages = ~60 movies
        r = http_requests.get(
            'https://api.themoviedb.org/3/movie/popular',
            params={'api_key': tmdb_key, 'page': page},
            timeout=10
        )
        if r.status_code != 200:
            break
        for m in r.json().get('results', []):
            movies.append({
                'title': m.get('title', ''),
                'desc': m.get('overview', ''),
                'year': (m.get('release_date') or '2000')[:4],
                'lang': m.get('original_language', 'en').upper(),
                'cover': 'https://image.tmdb.org/t/p/w500' + m['poster_path'] if m.get('poster_path') else '',
                'tmdb_id': str(m.get('id', ''))
            })

    conn = get_db()
    inserted = 0
    try:
        with conn.cursor() as cursor:
            for m in movies:
                if not m['title']:
                    continue
                cursor.execute(
                    "INSERT IGNORE INTO items (title,description,category,genre,release_year,language,cover_image,is_ethiopian,external_id) VALUES(%s,%s,'movie','Movie',%s,%s,%s,0,%s)",
                    (m['title'], m['desc'], m['year'], m['lang'], m['cover'], m['tmdb_id'])
                )
                cursor.execute("SELECT id FROM items WHERE title=%s AND category='movie'", (m['title'],))
                row = cursor.fetchone()
                if row:
                    cursor.execute(
                        "INSERT IGNORE INTO movie_details (item_id,director,cast_list,duration,tmdb_id) VALUES(%s,'','',0,%s)",
                        (row['id'], m['tmdb_id'])
                    )
                    inserted += 1
        conn.commit()
        return success_response(data={"inserted": inserted, "total": len(movies)}, message=f"Seeded {inserted} movies")
    finally:
        conn.close()
