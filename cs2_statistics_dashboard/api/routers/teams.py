from fastapi import APIRouter
import sqlite3

router = APIRouter()
DB = "database/cs2.db"

@router.get("/teams")
def get_teams():
    c = sqlite3.connect(DB)
    cur = c.cursor()
    cur.execute("SELECT name, logo_url FROM teams")
    rows = cur.fetchall()
    c.close()
    return [{"name": r[0], "logo": r[1]} for r in rows]

@router.post("/teams")
def add_team(name: str, logo_url: str):
    c = sqlite3.connect(DB)
    cur = c.cursor()
    cur.execute("INSERT INTO teams VALUES (NULL,?,?)", (name, logo_url))
    c.commit()
    c.close()

@router.delete("/teams")
def delete_team(name: str):
    c = sqlite3.connect(DB)
    cur = c.cursor()
    cur.execute("DELETE FROM teams WHERE name=?", (name,))
    c.commit()
    c.close()
