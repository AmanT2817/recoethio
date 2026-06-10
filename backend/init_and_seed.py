import pymysql
import os
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

load_dotenv()

conn = pymysql.connect(
    host=os.environ.get('MYSQLHOST', 'zephyr.proxy.rlwy.net'),
    port=int(os.environ.get('MYSQLPORT', 28935)),
    user=os.environ.get('MYSQLUSER', 'root'),
    password=os.environ.get('MYSQLPASSWORD'),
    database=os.environ.get('MYSQLDATABASE', 'railway'),
    cursorclass=pymysql.cursors.DictCursor,
    connect_timeout=30
)

with conn.cursor() as cur:
    print("→ Creating tables...")

    tables_sql = [
        """CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            role ENUM('user', 'admin') NOT NULL DEFAULT 'user',
            profile_picture VARCHAR(255),
            bio TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )""",

        """CREATE TABLE IF NOT EXISTS items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            category ENUM('movie', 'music', 'book') NOT NULL,
            genre VARCHAR(100),
            release_year YEAR,
            language VARCHAR(50) DEFAULT 'English',
            cover_image VARCHAR(255),
            is_ethiopian TINYINT(1) DEFAULT 0,
            external_id VARCHAR(100),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_category (category),
            INDEX idx_is_ethiopian (is_ethiopian)
        )""",

        """CREATE TABLE IF NOT EXISTS ratings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            item_id INT NOT NULL,
            score TINYINT NOT NULL CHECK (score BETWEEN 1 AND 5),
            review TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            UNIQUE KEY uq_user_item (user_id, item_id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
            INDEX idx_item_id (item_id)
        )""",

        """CREATE TABLE IF NOT EXISTS wishlist (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            item_id INT NOT NULL,
            added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY uq_wishlist (user_id, item_id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
        )""",
    ]

    for sql in tables_sql:
        cur.execute(sql)

    print("✓ Tables created!")
    print("→ Seeding data...")

    items = [
        ("Inception","Sci-Fi thriller about dream heist","movie","Sci-Fi",2010,"English","https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",0),
        ("The Dark Knight","Batman vs Joker","movie","Action",2008,"English","https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",0),
        ("Interstellar","Space exploration through wormhole","movie","Sci-Fi",2014,"English","https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",0),
        ("The Shawshank Redemption","Prison drama masterpiece","movie","Drama",1994,"English","",0),
        ("Forrest Gump","Life is like a box of chocolates","movie","Comedy",1994,"English","",0),
        ("Teza","Ethiopian intellectual returns home during Derg regime","movie","Drama",2008,"Amharic","",1),
        ("Difret","Ethiopian girl shoots abductor in self-defense","movie","Drama",2014,"Amharic","",1),
        ("Blinding Lights","Synth-pop hit by The Weeknd","music","Pop",2019,"English","",0),
        ("Bohemian Rhapsody","Queen masterpiece","music","Rock",1975,"English","",0),
        ("Shape of You","Ed Sheeran pop hit","music","Pop",2017,"English","",0),
        ("Tizita - Mahmoud Ahmed","Classic Ethiopian nostalgia song","music","Tizita",1975,"Amharic","",1),
        ("Tikur Sew - Teddy Afro","Iconic Ethiopian pop anthem","music","Ethiopian Pop",2012,"Amharic","",1),
        ("1984","Dystopian novel by George Orwell","book","Fiction",1949,"English","",0),
        ("The Alchemist","Journey to find personal legend","book","Fiction",1988,"English","",0),
        ("To Kill a Mockingbird","Classic American literature","book","Fiction",1960,"English","",0),
        ("Pride and Prejudice","Jane Austen romance","book","Romance",1813,"English","",0),
        ("Fikir Eske Mekabir","Classic Ethiopian love novel","book","Fiction",1966,"Amharic","",1),
        ("Oromay","Ethiopian novel about fall of Derg","book","Historical Fiction",1983,"Amharic","",1),
    ]

    for i in items:
        cur.execute("INSERT IGNORE INTO items (title,description,category,genre,release_year,language,cover_image,is_ethiopian) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", i)

    h = generate_password_hash("admin123")
    cur.execute("INSERT INTO users (username,email,password_hash,role) VALUES ('admin','admin@recoethio.com',%s,'admin') ON DUPLICATE KEY UPDATE password_hash=%s", (h,h))

    conn.commit()

conn.close()
print("✓ Done! Database initialized and seeded.")
