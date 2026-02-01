from fastapi import APIRouter
import sqlite3, hashlib

router = APIRouter()
DB = "database/cs2.db"

def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()

@router.post("/register")
def register(username: str, password: str):
    c = sqlite3.connect(DB)
    cur = c.cursor()
    cur.execute(
        "INSERT INTO users VALUES (NULL,?,?,?)",
        (username, hash_pw(password), "student")
    )
    c.commit()
    c.close()
    return {"status": "ok"}

@router.post("/login")
def login(username: str, password: str):
    c = sqlite3.connect(DB)
    cur = c.cursor()
    cur.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (username, hash_pw(password))
    )
    r = cur.fetchone()
    c.close()
    if r:
        return {"username": username, "role": r[0]}
    return {"error": "invalid"}
