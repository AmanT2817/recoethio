import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

conn = pymysql.connect(
    host=os.environ.get('MYSQLHOST'),
    port=int(os.environ.get('MYSQLPORT')),
    user=os.environ.get('MYSQLUSER'),
    password=os.environ.get('MYSQLPASSWORD'),
    database=os.environ.get('MYSQLDATABASE'),
    cursorclass=pymysql.cursors.DictCursor
)

MOVIES = [
    ("Atesheguatem Wey?", "Ethiopian drama exploring relationships and personal decisions.", "Drama", 2020),
    ("Fiker Endabede", "A story centered on love, sacrifice, and emotional challenges.", "Romance, Drama", 2018),
    ("Fre", "A widowed father fights to protect his daughter after a traumatic assault.", "Drama", 2017),
    ("Bilatena", "Coming-of-age story focusing on youth and social realities.", "Drama", 2016),
    ("Fetesh Agbign", "A romantic comedy involving marriage and misunderstandings.", "Comedy, Romance", 2015),
    ("Kebad Mizan", "A dramatic story about difficult choices and consequences.", "Drama", 2016),
    ("Yet Neber", "A love story involving separation and reunion.", "Romance", 2017),
    ("Tewedegnalech", "A romantic drama focused on commitment and emotional sacrifice.", "Romance, Drama", 2018),
    ("Sele Enat Lij", "Explores the bond between a mother and child.", "Family, Drama", 2017),
    ("Yamiral Hagere", "A story of identity, belonging, and Ethiopian culture.", "Drama", 2019),
    ("Ardibo", "A character-driven Ethiopian drama about life and relationships.", "Drama", 2018),
    ("Restaw", "Explores community life and personal struggles.", "Drama", 2019),
    ("Ewnet Alegn", "A story focused on truth, trust, and personal integrity.", "Drama", 2017),
    ("Condominiumu", "Life and relationships within Addis Ababa condominium communities.", "Drama, Comedy", 2016),
    ("Yesfera Lejoch", "A social drama centered on urban youth.", "Drama", 2018),
    ("Aman", "Personal and family struggles in modern Ethiopia.", "Drama", 2019),
    ("Adugna", "A story of determination and overcoming obstacles.", "Drama", 2017),
    ("Wech Guday", "Focuses on conflict and social issues.", "Drama", 2016),
    ("BeMengede Lay", "A journey of self-discovery and life lessons.", "Drama", 2018),
    ("Alsetem", "A character-driven story about regret and redemption.", "Drama", 2019),
    ("Hiroshima", "Ethiopian production inspired by consequences of conflict and war.", "Historical Drama", 2015),
    ("Ye Hizb Negn", "Focuses on society, leadership, and public responsibility.", "Political Drama", 2016),
    ("Pagume 7", "A story linked to Ethiopian social and political realities.", "Historical Drama", 2017),
    ("Hello Ethiopia", "A contemporary look at Ethiopian society and culture.", "Social Drama", 2019),
    ("3 Plus 1", "Humorous situations involving friendship and relationships.", "Comedy", 2016),
    ("Ye Arada Lij", "Classic Ethiopian urban comedy centered on street-smart characters.", "Comedy", 2014),
    ("Felashaw 2", "Sequel featuring comedic misunderstandings and adventures.", "Comedy", 2017),
    ("Bizu Tebazu", "A humorous take on everyday Ethiopian life.", "Comedy", 2018),
    ("Bombu Fikresh", "Love and comedy collide in unexpected ways.", "Romantic Comedy", 2019),
    ("Simet", "An Ethiopian drama exploring emotional and social challenges.", "Drama", 2020),
    ("Ye Wendoch Guday", "A highly rated Ethiopian drama following interpersonal relationships.", "Drama", 2007),
    ("Amalayu", "Personal struggles, family dynamics, and social expectations.", "Drama", 2013),
    ("Yilugnta", "A man juggling a fake marriage finds himself trapped between family expectations.", "Comedy, Romance, Drama", 2012),
    ("Atse Mandela", "Exploring themes of ambition, relationships, and personal growth.", "Drama", 2017),
    ("Aygebanim", "A dramatic story about love, family, and modern Ethiopian society.", "Drama", 2015),
    ("Anelakekem", "Personal relationships and consequences of life-changing decisions.", "Drama", 2014),
    ("Chefu", "A wealthy man falls for a poor young woman from Addis Ababa.", "Romance, Drama", 2012),
    ("Fidelawit", "A long-form Ethiopian drama examining family conflicts.", "Drama", 2016),
    ("Running Against the Wind", "Two Ethiopian friends pursue their dreams through determination.", "Drama, Sports", 2019),
    ("Kerbe", "A family torn apart after a traumatic crime exposes social stigma.", "Drama", 2021),
    ("Enchained", "Set in 1916 Ethiopia, two rivals face justice after a scandalous incident.", "Historical Drama", 2019),
    ("Taza", "A woman returning from Cuba struggles to reconnect with her homeland.", "Romance, Drama", 2017),
    ("Lambadina", "A young boy's journey from Addis Ababa across continents.", "Adventure, Drama", 2015),
    ("Min Alesh?", "A determined young girl uses athletics toward a brighter future.", "Drama, Sports", 2019),
    ("Price of Love", "A taxi driver entangled in a difficult relationship confronts his past.", "Drama, Romance", 2015),
    ("Sewenetwa", "Portrays Ethiopian women working abroad as domestic workers.", "Drama", 2019),
    ("Scar Chiret", "A man infected with rabies races against time to save his family.", "Horror, Thriller", 2022),
    ("Rebuni", "A businessman becomes emotionally involved with a landowner.", "Romance, Drama", 2015),
    ("Lomi Shita", "A family struggles with tragedy during 1970s Ethiopian political upheaval.", "Historical Drama", 2012),
    ("Criterion for Marriage", "A woman chooses between societal expectations and justice.", "Drama", 2022),
]

inserted = 0
skipped = 0

with conn.cursor() as cur:
    for title, desc, genre, year in MOVIES:
        cur.execute("SELECT id FROM items WHERE title=%s AND category='movie'", (title,))
        if cur.fetchone():
            skipped += 1
            continue
        cur.execute(
            "INSERT INTO items (title,description,category,genre,release_year,language,cover_image,is_ethiopian) VALUES(%s,%s,'movie',%s,%s,'Amharic','',1)",
            (title, desc, genre, year)
        )
        inserted += 1

conn.commit()
conn.close()
print(f"Done! Inserted: {inserted}, Skipped: {skipped}")
# New Ethiopian books, music, and additional movies
NEW_ITEMS = [
    # Books (title, desc, category, genre, year, language)
    ("Fikir Eske Mekaber", "One of Ethiopia's most beloved classic novels. A sweeping romantic story regarded as a cornerstone of modern Amharic literature.", "book", "Fiction, Romance", 1966, "Amharic"),
    ("Biltua Totit", "A new Amharic fiction book by Ethiopian author Alemayehu Kassa.", "book", "Fiction", 2025, "Amharic"),
    ("Melkamua Rut", "An Amharic book exploring the story of Ruth as a symbol of true friendship and loyalty.", "book", "Fiction, Biography", 2025, "Amharic"),
    ("Aksumawyan", "A book about the Aksumite civilization and its history.", "book", "History", 2025, "Amharic"),
    ("Amuadit Ena Gomadit", "A new Amharic fiction book by Sintayehu Tasew.", "book", "Fiction", 2025, "Amharic"),
    ("Teamire Mariam", "A major Ethiopian Orthodox religious text about the miracles of the Virgin Mary.", "book", "Religious", 2000, "Amharic"),
    # Music
    ("Efoy", "A 16-track Amharic music album by Asne Zuba.", "music", "Contemporary", 2022, "Amharic"),
    ("Etege Taitu", "An Amharic music album by Yezina Negash.", "music", "Amharic Music", 2020, "Amharic"),
    ("Majete", "An Amharic music album by Nina Girma.", "music", "Amharic Music", 2020, "Amharic"),
    ("Maal Mallisaa", "An Afan Oromo music album by Hacaaluu Hundessa.", "music", "Oromo Music", 2018, "Oromo"),
    ("Akisumawit", "A Tigirigna music album by Dawit Nega.", "music", "Tigrinya Music", 2019, "Tigrinya"),
    ("Fikir Tetsafe", "A 16-track spiritual song album by Bethelhem Tezera.", "music", "Christian Spiritual", 2022, "Amharic"),
    ("Abatinetih", "A Christian spiritual song by Hiwot Melese.", "music", "Christian Spiritual", 2022, "Amharic"),
    ("NEGUS", "A Christian spiritual worship song by Mesfin Mamo.", "music", "Christian Spiritual", 2020, "Amharic"),
    # Additional movies
    ("Atihijibign", "An Ethiopian romantic comedy starring Solomon Muhe and Semehal Tilahun.", "movie", "Romantic Comedy", 2019, "Amharic"),
    ("Fikir Simenezer", "An Ethiopian romantic comedy starring Solomon Bogale.", "movie", "Romantic Comedy", 2018, "Amharic"),
    ("Asertu Kenat", "An Ethiopian drama starring Fikadu H/Mariam.", "movie", "Drama", 2019, "Amharic"),
    ("Werk Bewerk", "An Ethiopian drama starring Helen Bedilu and Serawit Fikire.", "movie", "Drama", 2020, "Amharic"),
    ("Babilon", "An Ethiopian comedy starring Engida Getachew.", "movie", "Comedy", 2018, "Amharic"),
]

i2, s2 = 0, 0
with conn.cursor() as cur:
    for title, desc, cat, genre, year, lang in NEW_ITEMS:
        cur.execute("SELECT id FROM items WHERE title=%s AND category=%s", (title, cat))
        if cur.fetchone():
            s2 += 1
            continue
        cur.execute(
            "INSERT INTO items (title,description,category,genre,release_year,language,cover_image,is_ethiopian) VALUES(%s,%s,%s,%s,%s,%s,'',1)",
            (title, desc, cat, genre, year, lang)
        )
        i2 += 1
conn.commit()
conn.close()
print(f"New items - Inserted: {i2}, Skipped: {s2}")
