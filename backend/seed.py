"""
Seed script - populates the database with sample data.
Run with: python seed.py
"""
import pymysql
from werkzeug.security import generate_password_hash

conn = pymysql.connect(
    host='localhost', user='root', password='',
    database='recommendation_system',
    cursorclass=pymysql.cursors.DictCursor
)

movies = [
    ("Inception", "A thief who steals corporate secrets through dream-sharing technology.", "movie", "Sci-Fi", 2010, "English", "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg", 0),
    ("The Dark Knight", "Batman faces the Joker, a criminal mastermind who plunges Gotham into chaos.", "movie", "Action", 2008, "English", "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg", 0),
    ("Parasite", "A poor family schemes to become employed by a wealthy family.", "movie", "Thriller", 2019, "Korean", "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg", 0),
    ("Interstellar", "A team of explorers travel through a wormhole in space.", "movie", "Sci-Fi", 2014, "English", "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg", 0),
    ("The Lion King", "A young lion prince flees his kingdom after his father's murder.", "movie", "Animation", 1994, "English", "https://image.tmdb.org/t/p/w500/sKCr78MXSLixwmZ8DyJLrpMsd15.jpg", 0),
    ("Teza", "An Ethiopian intellectual returns home after years abroad during the Derg regime.", "movie", "Drama", 2008, "Amharic", "https://upload.wikimedia.org/wikipedia/en/thumb/4/4e/Teza_film.jpg/220px-Teza_film.jpg", 1),
    ("Difret", "A young Ethiopian girl shoots her abductor in self-defense and faces trial.", "movie", "Drama", 2014, "Amharic", "https://upload.wikimedia.org/wikipedia/en/thumb/0/0e/Difret_film_poster.jpg/220px-Difret_film_poster.jpg", 1),
    ("Lamb", "A childless couple in rural Ethiopia find a lost boy and decide to raise him.", "movie", "Drama", 2015, "Amharic", "", 1),
]

music = [
    ("Blinding Lights", "Synth-pop hit with retro 80s vibes.", "music", "Pop", 2019, "English", "https://upload.wikimedia.org/wikipedia/en/e/e6/The_Weeknd_-_Blinding_Lights.png", 0),
    ("Shape of You", "A catchy pop song about attraction and romance.", "music", "Pop", 2017, "English", "", 0),
    ("Bohemian Rhapsody", "A six-minute suite blending rock, opera, and ballad.", "music", "Rock", 1975, "English", "", 0),
    ("Despacito", "A reggaeton-pop song that became a global phenomenon.", "music", "Reggaeton", 2017, "Spanish", "", 0),
    ("Tizita - Mahmoud Ahmed", "A classic Ethiopian song expressing longing and nostalgia.", "music", "Tizita", 1975, "Amharic", "", 1),
    ("Ambassel - Tilahun Gessesse", "Traditional Ethiopian highland music with deep emotional resonance.", "music", "Ambassel", 1970, "Amharic", "", 1),
    ("Yegna - Lomi", "Modern Ethiopian pop music blending traditional and contemporary styles.", "music", "Ethiopian Pop", 2014, "Amharic", "", 1),
    ("Bati - Aster Aweke", "A beloved Ethiopian song in the Bati scale.", "music", "Bati", 1990, "Amharic", "", 1),
]

books = [
    ("To Kill a Mockingbird", "A story of racial injustice and childhood innocence in the American South.", "book", "Fiction", 1960, "English", "", 0),
    ("1984", "A dystopian novel about totalitarianism and surveillance.", "book", "Dystopian", 1949, "English", "", 0),
    ("The Alchemist", "A young shepherd's journey to find treasure and his personal legend.", "book", "Fiction", 1988, "English", "", 0),
    ("Atomic Habits", "A guide to building good habits and breaking bad ones.", "book", "Self-Help", 2018, "English", "", 0),
    ("Fikir Eske Mekabir", "A classic Ethiopian novel about love, tragedy, and society.", "book", "Fiction", 1966, "Amharic", "", 1),
    ("Oromay", "An Ethiopian novel depicting the fall of the Derg regime.", "book", "Historical Fiction", 1983, "Amharic", "", 1),
    ("Ye Hidar Anbessa", "A celebrated Ethiopian children's story.", "book", "Children", 1970, "Amharic", "", 1),
    ("The Beautiful Things That Heaven Bears", "An Ethiopian immigrant's life in Washington D.C.", "book", "Fiction", 2007, "English", "", 1),
]

movie_details = [
    (1, "Christopher Nolan", "Leonardo DiCaprio, Joseph Gordon-Levitt", 148),
    (2, "Christopher Nolan", "Christian Bale, Heath Ledger", 152),
    (3, "Bong Joon-ho", "Song Kang-ho, Lee Sun-kyun", 132),
    (4, "Christopher Nolan", "Matthew McConaughey, Anne Hathaway", 169),
    (5, "Roger Allers", "Matthew Broderick, Jeremy Irons", 88),
    (6, "Haile Gerima", "Aaron Arefe, Abiye Tedla", 140),
    (7, "Zeresenay Mehari", "Tizita Hagere, Meron Getnet", 99),
    (8, "Yared Zeleke", "Rediat Amare, Kidist Siyum", 94),
]

music_details = [
    (9, "The Weeknd", "After Hours", 200),
    (10, "Ed Sheeran", "Divide", 234),
    (11, "Queen", "A Night at the Opera", 354),
    (12, "Luis Fonsi", "Vida", 229),
    (13, "Mahmoud Ahmed", "Ere Mela Mela", 245, "Tizita"),
    (14, "Tilahun Gessesse", "Yematibela Wef", 312, "Ambassel"),
    (15, "Yegna", "Lomi", 198, "Ethiopian Pop"),
    (16, "Aster Aweke", "Kabu", 267, "Bati"),
]

book_details = [
    (17, "Harper Lee", "J. B. Lippincott & Co.", "978-0-06-112008-4", 281),
    (18, "George Orwell", "Secker & Warburg", "978-0-452-28423-4", 328),
    (19, "Paulo Coelho", "HarperOne", "978-0-06-231500-7", 208),
    (20, "James Clear", "Avery", "978-0-7352-1129-2", 320),
    (21, "Haddis Alemayehu", "Mega", "N/A", 450),
    (22, "Bealu Girma", "Kuraz", "N/A", 380),
    (23, "Unknown", "Ethiopian Publishers", "N/A", 120),
    (24, "Dinaw Mengestu", "Riverhead Books", "978-1-59448-998-9", 228),
]

ethiopian_items = [6, 7, 8, 13, 14, 15, 16, 21, 22, 23, 24]
ethiopian_metadata = [
    (6, "ጠዛ", "Addis Ababa", "historical,drama", 1),
    (7, "ድፍረት", "Addis Ababa", "drama,women-rights", 1),
    (8, "በግ", "Rural Ethiopia", "drama,family", 1),
    (13, "ትዝታ - ማህሙድ አህመድ", "Addis Ababa", "traditional,tizita", 1),
    (14, "አምባሰል - ጥላሁን ገሠሠ", "Addis Ababa", "traditional,ambassel", 1),
    (15, "የኛ - ሎሚ", "Addis Ababa", "modern,pop", 1),
    (16, "ባቲ - አስቴር አወቀ", "Addis Ababa", "traditional,bati", 1),
    (21, "ፍቅር እስከ መቃብር", "Addis Ababa", "classic,romance", 1),
    (22, "ኦሮማይ", "Addis Ababa", "historical,political", 1),
    (23, "የህዳር አንበሳ", "Addis Ababa", "children,traditional", 1),
    (24, "The Beautiful Things That Heaven Bears", "Washington D.C.", "diaspora,fiction", 1),
]

try:
    with conn.cursor() as cursor:
        # Insert items
        for item in movies + music + books:
            cursor.execute(
                """INSERT IGNORE INTO items (title, description, category, genre, release_year,
                   language, cover_image, is_ethiopian) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                item
            )

        # Movie details
        for d in movie_details:
            cursor.execute(
                "INSERT IGNORE INTO movie_details (item_id, director, cast_list, duration) VALUES (%s,%s,%s,%s)",
                d
            )

        # Music details (some have ethiopian_genre)
        for d in music_details:
            if len(d) == 5:
                cursor.execute(
                    "INSERT IGNORE INTO music_details (item_id, artist, album, duration, ethiopian_genre) VALUES (%s,%s,%s,%s,%s)", d
                )
            else:
                cursor.execute(
                    "INSERT IGNORE INTO music_details (item_id, artist, album, duration) VALUES (%s,%s,%s,%s)", d
                )

        # Book details
        for d in book_details:
            cursor.execute(
                "INSERT IGNORE INTO book_details (item_id, author, publisher, isbn, pages) VALUES (%s,%s,%s,%s,%s)", d
            )

        # Ethiopian metadata
        for d in ethiopian_metadata:
            cursor.execute(
                """INSERT IGNORE INTO ethiopian_content_metadata
                   (item_id, local_title, region, cultural_tags, verified) VALUES (%s,%s,%s,%s,%s)""", d
            )

        # Admin user with proper password hash
        admin_hash = generate_password_hash('admin123')
        cursor.execute(
            """INSERT INTO users (username, email, password_hash, role)
               VALUES ('admin', 'admin@uog.edu.et', %s, 'admin')
               ON DUPLICATE KEY UPDATE password_hash = %s""",
            (admin_hash, admin_hash)
        )

        conn.commit()
        print("✅ Database seeded successfully!")
        print("   - 8 movies (3 Ethiopian)")
        print("   - 8 music tracks (4 Ethiopian)")
        print("   - 8 books (4 Ethiopian)")
        print("   - Admin user: admin@uog.edu.et / admin123")

except Exception as e:
    print(f"❌ Error: {e}")
    conn.rollback()
finally:
    conn.close()
