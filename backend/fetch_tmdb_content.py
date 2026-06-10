import requests
import pymysql
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
TMDB_BASE_URL = "https://api.themoviedb.org/3"

conn = pymysql.connect(
    host=os.environ.get('MYSQLHOST'),
    port=int(os.environ.get('MYSQLPORT')),
    user=os.environ.get('MYSQLUSER'),
    password=os.environ.get('MYSQLPASSWORD'),
    database=os.environ.get('MYSQLDATABASE'),
    cursorclass=pymysql.cursors.DictCursor,
    connect_timeout=30
)

def fetch_international_blockbusters():
    """Fetch top international blockbuster movies"""
    movies = []
    seen_ids = set()

    urls = [
        f"{TMDB_BASE_URL}/movie/popular",
        f"{TMDB_BASE_URL}/movie/top_rated",
        f"{TMDB_BASE_URL}/movie/upcoming"
    ]

    try:
        for url in urls:
            for page in range(1, 6):  # Get 5 pages from each endpoint
                params = {
                    'api_key': TMDB_API_KEY,
                    'language': 'en-US',
                    'page': page
                }
                resp = requests.get(url, params=params, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    for movie in data.get('results', []):
                        movie_id = movie.get('id')
                        if movie.get('poster_path') and movie_id not in seen_ids:
                            seen_ids.add(movie_id)
                            movies.append({
                                'title': movie.get('title', 'Unknown'),
                                'description': movie.get('overview', ''),
                                'release_year': movie.get('release_date', '')[:4] if movie.get('release_date') else 2024,
                                'cover_image': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}",
                                'external_id': movie.get('id'),
                                'is_ethiopian': 0
                            })
        print(f"✓ Fetched {len(movies)} international movies")
    except Exception as e:
        print(f"✗ Error fetching international movies: {e}")

    return movies

def fetch_international_movies():
    """Fetch popular international movies"""
    movies = []

    url = f"{TMDB_BASE_URL}/movie/popular"
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'en-US',
        'sort_by': 'popularity.desc'
    }

    try:
        for page in range(1, 2):  # Get first page (20 movies)
            params['page'] = page
            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                for movie in data.get('results', [])[:50]:  # Limit to 50
                    if movie.get('poster_path'):
                        movies.append({
                            'title': movie.get('title', 'Unknown'),
                            'description': movie.get('overview', ''),
                            'release_year': movie.get('release_date', '')[:4] if movie.get('release_date') else 2024,
                            'cover_image': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}",
                            'external_id': movie.get('id'),
                            'is_ethiopian': 0
                        })
        print(f"✓ Fetched {len(movies)} international movies")
    except Exception as e:
        print(f"✗ Error fetching international movies: {e}")

    return movies

def add_movies_to_db(movies):
    """Add movies to database"""
    count = 0
    try:
        with conn.cursor() as cur:
            for movie in movies:
                try:
                    cur.execute("""
                        INSERT IGNORE INTO items
                        (title, description, category, genre, release_year, language, cover_image, is_ethiopian, external_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        movie['title'],
                        movie['description'],
                        'movie',
                        'General',
                        movie['release_year'],
                        'Amharic' if movie['is_ethiopian'] else 'English',
                        movie['cover_image'],
                        movie['is_ethiopian'],
                        movie['external_id']
                    ))
                    count += 1
                except Exception as e:
                    print(f"Error adding {movie['title']}: {e}")

            conn.commit()
        print(f"✓ Added {count} movies to database")
    except Exception as e:
        print(f"✗ Error adding movies: {e}")

if __name__ == '__main__':
    print("→ Fetching international movies from TMDB...")

    international_movies = fetch_international_blockbusters()

    print(f"→ Adding {len(international_movies)} movies to database...")
    add_movies_to_db(international_movies)

    conn.close()
    print("✓ TMDB content import complete!")
