import pymysql
import os
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

# Extended content list: (title, description, category, genre, release_year, language, cover_image, is_ethiopian)
content = [
    # ETHIOPIAN MOVIES
    ("Teza","Ethiopian intellectual returns home during Derg regime","movie","Drama",2008,"Amharic","",1),
    ("Difret","Ethiopian girl shoots abductor in self-defense","movie","Drama",2014,"Amharic","",1),
    ("Haile","Life of Ethiopian running legend Haile Gebrselassie","movie","Documentary",2016,"English/Amharic","",1),
    ("Lamb","A young girl navigates family traditions and modernity","movie","Drama",2015,"Amharic","",1),
    ("Bajaj Days","Coming of age in Addis Ababa","movie","Drama",2014,"Amharic","",1),
    ("Hellina Wuba","Ethiopian folk stories told through cinema","movie","Drama",2009,"Amharic","",1),
    ("Stitches","Ethiopian diaspora returns home","movie","Drama",2013,"Amharic","",1),
    ("Addis Ababa, I Love You","Urban tales from the capital","movie","Drama",2012,"Amharic","",1),

    # INTERNATIONAL MOVIES - DRAMA
    ("The Shawshank Redemption","Prison drama masterpiece","movie","Drama",1994,"English","",0),
    ("Forrest Gump","Life is like a box of chocolates","movie","Comedy",1994,"English","",0),
    ("The Pursuit of Happyness","Father's struggle to build better life","movie","Drama",2006,"English","",0),
    ("Life is Beautiful","Italian masterpiece about hope in darkness","movie","Drama",1997,"Italian","",0),
    ("Parasite","Korean thriller about class divide","movie","Thriller",2019,"Korean","",0),
    ("12 Angry Men","Jury deliberation masterpiece","movie","Drama",1957,"English","",0),

    # INTERNATIONAL MOVIES - SCI-FI
    ("Inception","Sci-Fi thriller about dream heist","movie","Sci-Fi",2010,"English","",0),
    ("The Dark Knight","Batman vs Joker","movie","Action",2008,"English","",0),
    ("Interstellar","Space exploration through wormhole","movie","Sci-Fi",2014,"English","",0),
    ("Blade Runner 2049","Sci-Fi noir masterpiece","movie","Sci-Fi",2017,"English","",0),
    ("The Matrix","Reality-bending sci-fi classic","movie","Sci-Fi",1999,"English","",0),
    ("Dune","Epic space opera","movie","Sci-Fi",2021,"English","",0),

    # INTERNATIONAL MOVIES - ACTION
    ("Mad Max Fury Road","High-octane action spectacle","movie","Action",2015,"English","",0),
    ("John Wick","Assassin revenge thriller","movie","Action",2014,"English","",0),
    ("Mission Impossible Fallout","Spy action thriller","movie","Action",2018,"English","",0),

    # INTERNATIONAL MOVIES - ROMANCE
    ("Pride and Prejudice","Jane Austen classic romance","movie","Romance",2005,"English","",0),
    ("The Notebook","Romantic drama","movie","Romance",2004,"English","",0),
    ("Titanic","Epic romance and disaster","movie","Romance",1997,"English","",0),

    # ETHIOPIAN MUSIC - TRADITIONAL
    ("Tizita - Mahmoud Ahmed","Classic Ethiopian nostalgia song","music","Tizita",1975,"Amharic","",1),
    ("Tikur Sew - Teddy Afro","Iconic Ethiopian pop anthem","music","Ethiopian Pop",2012,"Amharic","",1),
    ("Yetom - Aster Aweke","Ethiopian jazz classic","music","Jazz",1988,"Amharic","",1),
    ("Ere Mela Mela - Tilahun Gessesse","Golden age Ethiopian music","music","Traditional",1970,"Amharic","",1),
    ("Belew Nesh - Mulatu Astatke","Father of Ethio-jazz","music","Jazz",1973,"Amharic","",1),
    ("Addis Red Sea - Various Artists","Modern Ethiopian compilation","music","Ethiopian Pop",2010,"Amharic","",1),
    ("Lela - Gigi","Contemporary Ethiopian singer","music","Pop",2018,"Amharic","",1),
    ("Weyewa - Abebe Bikila","Sports-inspired Ethiopian music","music","Pop",2000,"Amharic","",1),

    # INTERNATIONAL MUSIC - POP
    ("Blinding Lights","Synth-pop hit by The Weeknd","music","Pop",2019,"English","",0),
    ("Shape of You","Ed Sheeran pop hit","music","Pop",2017,"English","",0),
    ("Levitating","Dua Lipa pop anthem","music","Pop",2020,"English","",0),
    ("As It Was","Harry Styles hit","music","Pop",2022,"English","",0),
    ("Anti-Hero","Taylor Swift","music","Pop",2022,"English","",0),

    # INTERNATIONAL MUSIC - ROCK
    ("Bohemian Rhapsody","Queen masterpiece","music","Rock",1975,"English","",0),
    ("Stairway to Heaven","Led Zeppelin classic","music","Rock",1971,"English","",0),
    ("Comfortably Numb","Pink Floyd","music","Rock",1979,"English","",0),
    ("Hotel California","Eagles","music","Rock",1976,"English","",0),

    # INTERNATIONAL MUSIC - HIP-HOP
    ("Lose Yourself","Eminem","music","Hip-Hop",2002,"English","",0),
    ("God's Plan","Drake","music","Hip-Hop",2018,"English","",0),
    ("Humble","Kendrick Lamar","music","Hip-Hop",2017,"English","",0),

    # INTERNATIONAL MUSIC - JAZZ
    ("Take Five","Dave Brubeck","music","Jazz",1959,"English","",0),
    ("Clair de Lune","Miles Davis","music","Jazz",1960,"English","",0),

    # ETHIOPIAN BOOKS
    ("Fikir Eske Mekabir","Classic Ethiopian love novel","book","Fiction",1966,"Amharic","",1),
    ("Oromay","Ethiopian novel about fall of Derg","book","Historical Fiction",1983,"Amharic","",1),
    ("Adwa","Ethiopian historical epic","book","Historical Fiction",2006,"Amharic","",1),
    ("Ge'ez Literature Collection","Ancient Ethiopian religious texts","book","Religious",400,"Ge'ez","",1),
    ("The Beautiful Ones Are Not Yet Born","Modern Ethiopian literature","book","Fiction",2008,"Amharic","",1),
    ("Fiker Ketema","Ethiopian poetry collection","book","Poetry",1990,"Amharic","",1),

    # INTERNATIONAL BOOKS - CLASSICS
    ("1984","Dystopian novel by George Orwell","book","Fiction",1949,"English","",0),
    ("The Alchemist","Journey to find personal legend","book","Fiction",1988,"English","",0),
    ("To Kill a Mockingbird","Classic American literature","book","Fiction",1960,"English","",0),
    ("Pride and Prejudice","Jane Austen romance","book","Romance",1813,"English","",0),
    ("The Great Gatsby","Jazz age classic","book","Fiction",1925,"English","",0),
    ("Wuthering Heights","Gothic romance","book","Romance",1847,"English","",0),

    # INTERNATIONAL BOOKS - MODERN
    ("The Midnight Library","Contemporary fiction","book","Fiction",2020,"English","",0),
    ("Project Hail Mary","Sci-Fi adventure","book","Sci-Fi",2021,"English","",0),
    ("Atomic Habits","Self-help bestseller","book","Self-Help",2018,"English","",0),
    ("Educated","Memoir","book","Biography",2018,"English","",0),

    # INTERNATIONAL BOOKS - FANTASY
    ("The Hobbit","Fantasy adventure","book","Fantasy",1937,"English","",0),
    ("Harry Potter and the Philosopher's Stone","Magical fantasy","book","Fantasy",1998,"English","",0),
    ("The Lord of the Rings","Epic fantasy","book","Fantasy",1954,"English","",0),

    # INTERNATIONAL BOOKS - MYSTERY
    ("The Girl with the Dragon Tattoo","Crime thriller","book","Mystery",2005,"Swedish","",0),
    ("Sherlock Holmes Collection","Mystery classics","book","Mystery",1892,"English","",0),
]

with conn.cursor() as cur:
    count = 0
    for item in content:
        try:
            cur.execute(
                "INSERT IGNORE INTO items (title,description,category,genre,release_year,language,cover_image,is_ethiopian) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                item
            )
            count += 1
        except Exception as e:
            print(f"Error adding {item[0]}: {e}")

    conn.commit()
    print(f"Added {count} items successfully!")

conn.close()
print("Bulk content seeding complete!")
