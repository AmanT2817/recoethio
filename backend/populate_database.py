import requests, pymysql, csv, os
from werkzeug.security import generate_password_hash

TMDB_API_KEY = "0f5d3d2056b3a0c9b8a58cd3f189c105"
SPOTIFY_CLIENT_ID = "e3514172c1554ed99d6983b20d868334"
SPOTIFY_CLIENT_SECRET = "9e6de3485b1242c4be4ab0ce539ffc4b"

DB = dict(host="localhost", user="root", password="",
          database="recommendation_system",
          cursorclass=pymysql.cursors.DictCursor)

def get_conn():
    return pymysql.connect(**DB)

def insert_item(cur, title, desc, cat, genre, year, lang, cover, eth, ext=""):
    cur.execute(
        "INSERT IGNORE INTO items (title,description,category,genre,release_year,language,cover_image,is_ethiopian,external_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (title, desc, cat, genre, year, lang, cover, eth, ext))
    cur.execute("SELECT id FROM items WHERE title=%s AND category=%s", (title, cat))
    row = cur.fetchone()
    return row["id"] if row else None
