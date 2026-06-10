import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

conn = pymysql.connect(
    host=os.environ.get('MYSQLHOST'),
    port=int(os.environ.get('MYSQLPORT')),
    user=os.environ.get('MYSQLUSER'),
    password=os.environ.get('MYSQLPASSWORD'),
    database=os.environ.get('MYSQLDATABASE'),
    cursorclass=pymysql.cursors.DictCursor,
    connect_timeout=30
)

with conn.cursor() as cur:
    print("Creating detail tables...")

    tables_sql = [
        """CREATE TABLE IF NOT EXISTS book_details (
            id INT AUTO_INCREMENT PRIMARY KEY,
            item_id INT NOT NULL UNIQUE,
            author VARCHAR(255),
            publisher VARCHAR(255),
            isbn VARCHAR(20),
            pages INT,
            FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
        )""",

        """CREATE TABLE IF NOT EXISTS movie_details (
            id INT AUTO_INCREMENT PRIMARY KEY,
            item_id INT NOT NULL UNIQUE,
            director VARCHAR(255),
            cast_list TEXT,
            duration INT COMMENT 'Duration in minutes',
            tmdb_id VARCHAR(50),
            FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
        )""",

        """CREATE TABLE IF NOT EXISTS music_details (
            id INT AUTO_INCREMENT PRIMARY KEY,
            item_id INT NOT NULL UNIQUE,
            artist VARCHAR(255),
            album VARCHAR(255),
            duration INT COMMENT 'Duration in seconds',
            spotify_id VARCHAR(100),
            ethiopian_genre VARCHAR(100) COMMENT 'e.g. Tizita, Bati, Anchihoye',
            FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
        )""",

        """CREATE TABLE IF NOT EXISTS preferences (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL UNIQUE,
            fav_genres VARCHAR(255) COMMENT 'Comma-separated genre preferences',
            fav_categories VARCHAR(100) COMMENT 'movie, music, book preferences',
            mood VARCHAR(50),
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )""",

        """CREATE TABLE IF NOT EXISTS recommendations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            item_id INT NOT NULL,
            score FLOAT NOT NULL COMMENT 'Algorithm confidence score',
            algorithm ENUM('collaborative', 'content_based', 'hybrid') NOT NULL,
            explanation TEXT,
            is_seen TINYINT(1) DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
            INDEX idx_user_id (user_id)
        )""",

        """CREATE TABLE IF NOT EXISTS ethiopian_content_metadata (
            id INT AUTO_INCREMENT PRIMARY KEY,
            item_id INT NOT NULL UNIQUE,
            local_title VARCHAR(255) COMMENT 'Title in Amharic',
            region VARCHAR(100) COMMENT 'e.g. Amhara, Tigray, Oromia',
            cultural_tags VARCHAR(255) COMMENT 'e.g. traditional, modern, folk',
            verified TINYINT(1) DEFAULT 0 COMMENT 'Manually verified by admin',
            added_by INT COMMENT 'Admin user ID who added this',
            FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
            FOREIGN KEY (added_by) REFERENCES users(id) ON DELETE SET NULL
        )""",
    ]

    for sql in tables_sql:
        try:
            cur.execute(sql)
            print("Created table")
        except Exception as e:
            if "already exists" in str(e):
                print("Table already exists")
            else:
                print(f"Error: {e}")

    conn.commit()

conn.close()
print("Done! Tables created.")
