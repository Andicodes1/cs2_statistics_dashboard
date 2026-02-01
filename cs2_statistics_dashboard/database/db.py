import sqlite3
import pandas as pd
import hashlib

DB = "database/cs2.db"

def connect():
    return sqlite3.connect(DB, check_same_thread=False)

def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()

def init_db():
    c = connect()
    cur = c.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        logo_url TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        team TEXT,
        opponent TEXT,
        map TEXT,
        result TEXT,
        event TEXT
    )
    """)

    c.commit()
    c.close()

def seed_admin():
    c = connect()
    cur = c.cursor()
    try:
        cur.execute(
            "INSERT INTO users VALUES (NULL,?,?,?)",
            ("admin", hash_pw("admin123"), "admin")
        )
    except:
        pass
    c.commit()
    c.close()

def seed_matches():
    c = connect()
    df = pd.read_csv("data/cs2_matches.csv")
    df.to_sql("matches", c, if_exists="replace", index=False)
    c.close()

def seed_teams():
    teams = [
        ("NAVI", "https://static.hltv.org/images/team/logo/4608"),
        ("G2", "https://static.hltv.org/images/team/logo/5995"),
        ("FAZE", "https://static.hltv.org/images/team/logo/6667"),
        ("VITALITY", "https://static.hltv.org/images/team/logo/9565"),
        ("SPIRIT", "https://static.hltv.org/images/team/logo/7020"),
        ("HEROIC", "https://static.hltv.org/images/team/logo/7175"),
        ("MOUZ", "https://static.hltv.org/images/team/logo/4494"),
        ("ASTRALIS", "https://static.hltv.org/images/team/logo/6665"),
        ("CLOUD9", "https://static.hltv.org/images/team/logo/5752"),
        ("FNATIC", "https://static.hltv.org/images/team/logo/4991"),
        ("BAD NEWS EAGLES", "https://static.hltv.org/images/team/logo/10917"),
    ]

    c = connect()
    cur = c.cursor()
    for t in teams:
        try:
            cur.execute("INSERT INTO teams (name, logo_url) VALUES (?,?)", t)
        except:
            pass
    c.commit()
    c.close()
