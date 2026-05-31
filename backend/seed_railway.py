import pymysql
from werkzeug.security import generate_password_hash

conn = pymysql.connect(
    host='ballast.proxy.rlwy.net',
    port=28244,
    user='root',
    password='EZvQeLKifXcWnffquIaYSolGQMUnbqIO',
    database='railway',
    cursorclass=pymysql.cursors.DictCursor,
    ssl={'ssl': {}},
    connect_timeout=30
)

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

with conn.cursor() as cur:
    for i in items:
        cur.execute("INSERT IGNORE INTO items (title,description,category,genre,release_year,language,cover_image,is_ethiopian) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", i)
    h = generate_password_hash("admin123")
    cur.execute("INSERT INTO users (username,email,password_hash,role) VALUES ('admin','admin@recoethio.com',%s,'admin') ON DUPLICATE KEY UPDATE password_hash=%s", (h,h))
conn.commit()
conn.close()
print("Done! Railway seeded.")
