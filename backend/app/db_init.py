"""
Database initialization - creates tables on app startup if they don't exist.
"""
import pymysql
import time
from flask import current_app

def init_db():
    """Initialize database schema if tables don't exist with retry logic."""
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            conn_params = {
                "host": current_app.config['MYSQL_HOST'],
                "user": current_app.config['MYSQL_USER'],
                "password": current_app.config['MYSQL_PASSWORD'],
                "database": current_app.config['MYSQL_DB'],
                "port": current_app.config['MYSQL_PORT'],
                "connect_timeout": 10,
                "read_timeout": 30,
                "write_timeout": 30,
                "autocommit": False
            }
            
            if current_app.config.get('MYSQL_SSL', False):
                conn_params['ssl_disabled'] = False
                conn_params['ssl_verify_cert'] = False
                conn_params['ssl_verify_identity'] = False
            
            conn = pymysql.connect(**conn_params)
            
            with conn.cursor() as cursor:
                # Check if items table exists
                cursor.execute("SELECT COUNT(*) FROM information_schema.TABLES WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'items'", 
                             (current_app.config['MYSQL_DB'],))
                if cursor.fetchone()[0] > 0:
                    print("✓ Database tables already exist")
                    conn.close()
                    return
                
                print("→ Creating database tables...")
                
                # Create all tables
                tables_sql = [
                    # TABLE 1: users
                    """CREATE TABLE users (
                        id              INT AUTO_INCREMENT PRIMARY KEY,
                        username        VARCHAR(50)  NOT NULL UNIQUE,
                        email           VARCHAR(100) NOT NULL UNIQUE,
                        password_hash   VARCHAR(255) NOT NULL,
                        role            ENUM('user', 'admin') NOT NULL DEFAULT 'user',
                        profile_picture VARCHAR(255),
                        bio             TEXT,
                        created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    )""",
                    
                    # TABLE 2: items
                    """CREATE TABLE items (
                        id              INT AUTO_INCREMENT PRIMARY KEY,
                        title           VARCHAR(255) NOT NULL,
                        description     TEXT,
                        category        ENUM('movie', 'music', 'book') NOT NULL,
                        genre           VARCHAR(100),
                        release_year    YEAR,
                        language        VARCHAR(50) DEFAULT 'English',
                        cover_image     VARCHAR(255),
                        is_ethiopian    TINYINT(1)  DEFAULT 0,
                        external_id     VARCHAR(100),
                        created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
                        INDEX idx_category (category),
                        INDEX idx_is_ethiopian (is_ethiopian)
                    )""",
                    
                    # TABLE 3: book_details
                    """CREATE TABLE book_details (
                        id          INT AUTO_INCREMENT PRIMARY KEY,
                        item_id     INT NOT NULL UNIQUE,
                        author      VARCHAR(255),
                        publisher   VARCHAR(255),
                        isbn        VARCHAR(20),
                        pages       INT,
                        FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
                    )""",
                    
                    # TABLE 4: movie_details
                    """CREATE TABLE movie_details (
                        id          INT AUTO_INCREMENT PRIMARY KEY,
                        item_id     INT NOT NULL UNIQUE,
                        director    VARCHAR(255),
                        cast_list   TEXT,
                        duration    INT COMMENT 'Duration in minutes',
                        tmdb_id     VARCHAR(50),
                        FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
                    )""",
                    
                    # TABLE 5: music_details
                    """CREATE TABLE music_details (
                        id              INT AUTO_INCREMENT PRIMARY KEY,
                        item_id         INT NOT NULL UNIQUE,
                        artist          VARCHAR(255),
                        album           VARCHAR(255),
                        duration        INT COMMENT 'Duration in seconds',
                        spotify_id      VARCHAR(100),
                        ethiopian_genre VARCHAR(100) COMMENT 'e.g. Tizita, Bati, Anchihoye',
                        FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
                    )""",
                    
                    # TABLE 6: ratings
                    """CREATE TABLE ratings (
                        id          INT AUTO_INCREMENT PRIMARY KEY,
                        user_id     INT NOT NULL,
                        item_id     INT NOT NULL,
                        score       TINYINT NOT NULL CHECK (score BETWEEN 1 AND 5),
                        review      TEXT,
                        created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        UNIQUE KEY uq_user_item (user_id, item_id),
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                        FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
                        INDEX idx_item_id (item_id)
                    )""",
                    
                    # TABLE 7: preferences
                    """CREATE TABLE preferences (
                        id              INT AUTO_INCREMENT PRIMARY KEY,
                        user_id         INT NOT NULL UNIQUE,
                        fav_genres      VARCHAR(255) COMMENT 'Comma-separated genre preferences',
                        fav_categories  VARCHAR(100) COMMENT 'movie, music, book preferences',
                        mood            VARCHAR(50),
                        updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )""",
                    
                    # TABLE 8: recommendations
                    """CREATE TABLE recommendations (
                        id              INT AUTO_INCREMENT PRIMARY KEY,
                        user_id         INT NOT NULL,
                        item_id         INT NOT NULL,
                        score           FLOAT NOT NULL COMMENT 'Algorithm confidence score',
                        algorithm       ENUM('collaborative', 'content_based', 'hybrid') NOT NULL,
                        explanation     TEXT,
                        is_seen         TINYINT(1) DEFAULT 0,
                        created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                        FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
                        INDEX idx_user_id (user_id)
                    )""",
                    
                    # TABLE 9: wishlist
                    """CREATE TABLE wishlist (
                        id          INT AUTO_INCREMENT PRIMARY KEY,
                        user_id     INT NOT NULL,
                        item_id     INT NOT NULL,
                        added_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE KEY uq_wishlist (user_id, item_id),
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                        FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
                    )""",
                    
                    # TABLE 10: ethiopian_content_metadata
                    """CREATE TABLE ethiopian_content_metadata (
                        id              INT AUTO_INCREMENT PRIMARY KEY,
                        item_id         INT NOT NULL UNIQUE,
                        local_title     VARCHAR(255) COMMENT 'Title in Amharic',
                        region          VARCHAR(100) COMMENT 'e.g. Amhara, Tigray, Oromia',
                        cultural_tags   VARCHAR(255) COMMENT 'e.g. traditional, modern, folk',
                        verified        TINYINT(1) DEFAULT 0 COMMENT 'Manually verified by admin',
                        added_by        INT COMMENT 'Admin user ID who added this',
                        FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
                        FOREIGN KEY (added_by) REFERENCES users(id) ON DELETE SET NULL
                    )""",
                ]
                
                for sql in tables_sql:
                    try:
                        cursor.execute(sql)
                    except pymysql.err.ProgrammingError as e:
                        if "already exists" in str(e):
                            pass  # Table already exists, continue
                        else:
                            raise
                
                conn.commit()
                print("✓ Database tables created successfully!")
            
            conn.close()
            return
            
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print(f"✗ Database connection error (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s, 4s
            else:
                print("✗ Failed to initialize database after retries")
        except Exception as e:
            print(f"✗ Database initialization error: {str(e)}")
            return
