import pymysql
from dotenv import load_dotenv
import os
load_dotenv()

conn = pymysql.connect(
    host=os.environ.get('MYSQLHOST'), port=int(os.environ.get('MYSQLPORT')),
    user=os.environ.get('MYSQLUSER'), password=os.environ.get('MYSQLPASSWORD'),
    database=os.environ.get('MYSQLDATABASE'), cursorclass=pymysql.cursors.DictCursor
)

ITEMS = [
    ("Efoy","16-track Amharic album by Asne Zuba.","music","Amharic Contemporary",2022,"Amharic"),
    ("Etege Taitu","Amharic music album by Yezina Negash.","music","Amharic Contemporary",2021,"Amharic"),
    ("Majete","Amharic music album by Nina Girma.","music","Amharic Contemporary",2022,"Amharic"),
    ("Azmach","Amharic music album by Henok Mehari.","music","Amharic Contemporary",2021,"Amharic"),
    ("Etemete","Amharic music album by Rahel Getu.","music","Amharic Contemporary",2021,"Amharic"),
    ("Haset","Amharic music album by Miky Haset.","music","Amharic Contemporary",2021,"Amharic"),
    ("Sibet","Amharic music album by Sami Dan.","music","Amharic Contemporary",2021,"Amharic"),
    ("Atigebam Alugn","Amharic music album by Lij Michael Faf.","music","Amharic Contemporary",2021,"Amharic"),
    ("Yetamene","Amharic music album by Haile Roots.","music","Amharic Contemporary",2021,"Amharic"),
    ("Atishishi Jember","Amharic music album by Meselu Fantahun.","music","Amharic Contemporary",2021,"Amharic"),
    ("Yene Zema","Amharic music album by Dawit Tsige.","music","Amharic Contemporary",2020,"Amharic"),
    ("Yene New","Amharic music album by PAMFALON.","music","Amharic Contemporary",2019,"Amharic"),
    ("Esatu Seat","Amharic music album by Leul Hailu.","music","Amharic Contemporary",2019,"Amharic"),
    ("Chelina","Amharic music album by Chelina.","music","Amharic Contemporary",2019,"Amharic"),
    ("Wedefit","Amharic music album by Bizuayehu Kifle.","music","Amharic Contemporary",2019,"Amharic"),
    ("Sew","Amharic music album by Tsedi.","music","Amharic Contemporary",2019,"Amharic"),
    ("Litegnabet","Amharic music album by Asefu Debalke.","music","Amharic Contemporary",2019,"Amharic"),
    ("Kemesha","Amharic music album by Hamelmal Abate.","music","Amharic Contemporary",2019,"Amharic"),
    ("Hid Zeyirat","Amharic music album by Abush Zeleke.","music","Amharic Contemporary",2019,"Amharic"),
    ("Chewa","Amharic music album by legendary singer Aster Aweke.","music","Amharic Contemporary",2019,"Amharic"),
    ("Balambaras","Amharic music album by Jacky Gosee.","music","Amharic Contemporary",2019,"Amharic"),
    ("Eninegager","Amharic music album by Abel Mulgeta.","music","Amharic Contemporary",2019,"Amharic"),
    ("Siyamsh Yamegnal","Amharic music album by Gosaye Tesfaye.","music","Amharic Contemporary",2019,"Amharic"),
    ("Sim Yelatim","Amharic music album by Dawit Senbeta.","music","Amharic Contemporary",2018,"Amharic"),
    ("Wegegta","Amharic music album by Betty G.","music","Amharic Contemporary",2018,"Amharic"),
    ("Netsbirak","Amharic music album by Rophnan.","music","Amharic Contemporary",2018,"Amharic"),
    ("Arada","Amharic music album by Teddy Yo.","music","Amharic Contemporary",2018,"Amharic"),
    ("ETHIOPIA","Patriotic Amharic album by Teddy Afro.","music","Amharic Patriotic",2017,"Amharic"),
    ("Yan Gize","Amharic music album by Addis Gurmesa.","music","Amharic Contemporary",2017,"Amharic"),
    ("Erotalehu","Amharic music album by the late singer Eyob Mekonnen.","music","Amharic Contemporary",2017,"Amharic"),
    ("Yene Habesha","Amharic music album by Aby Lakew.","music","Amharic Contemporary",2017,"Amharic"),
    ("Fikir Tetsafe","16-track spiritual song album by Bethelhem Tezera.","music","Christian Spiritual",2022,"Amharic"),
    ("Abatinetih","Christian spiritual song by Hiwot Melese.","music","Christian Spiritual",2022,"Amharic"),
    ("NEGUS","Christian spiritual worship song by Mesfin Mamo.","music","Christian Spiritual",2020,"Amharic"),
    ("Maal Mallisaa","Afan Oromo music album by Hacaaluu Hundessa.","music","Oromo Music",2018,"Oromo"),
    ("Gedaan Kenaaya","Afan Oromo music album by Taddalaa Gammadaa.","music","Oromo Music",2019,"Oromo"),
    ("Sanyii Mootii","Afan Oromo music album by Jamboo Joote.","music","Oromo Music",2018,"Oromo"),
    ("Akisumawit","Tigirigna music album by Dawit Nega.","music","Tigrinya Music",2019,"Tigrinya"),
    ("Gize","Tigirigna music album by Abebe Araya.","music","Tigrinya Music",2020,"Tigrinya"),
    ("Wesen","Tigirigna music album by Eden G/Silase.","music","Tigrinya Music",2019,"Tigrinya"),
    ("Fikir Eske Mekaber","Ethiopia's most celebrated novel Love Until the Grave by Hadis Alemayehu.","book","Fiction, Romance",1966,"Amharic"),
    ("Teamire Mariam","Major Ethiopian Orthodox religious text on miracles of the Virgin Mary.","book","Religious",2000,"Amharic"),
    ("Biltua Totit","New 2025 Amharic fiction book by Alemayehu Kassa.","book","Fiction",2025,"Amharic"),
    ("Melkamua Rut","Amharic book on the story of Ruth as a symbol of friendship and loyalty.","book","Fiction, Christian",2025,"Amharic"),
    ("Aksumawyan","Amharic book about the Aksumite civilization.","book","History",2025,"Amharic"),
    ("Amuadit Ena Gomadit","2025 Amharic fiction book by Sintayehu Tasew.","book","Fiction",2025,"Amharic"),
]

i, s = 0, 0
with conn.cursor() as cur:
    for title, desc, cat, genre, year, lang in ITEMS:
        cur.execute("SELECT id FROM items WHERE title=%s AND category=%s", (title, cat))
        if cur.fetchone():
            s += 1
            continue
        cur.execute("INSERT INTO items (title,description,category,genre,release_year,language,cover_image,is_ethiopian) VALUES(%s,%s,%s,%s,%s,%s,'',1)", (title, desc, cat, genre, year, lang))
        i += 1
conn.commit()
conn.close()
print(f"Done! Inserted: {i}, Skipped: {s}")
