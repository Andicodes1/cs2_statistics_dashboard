from fastapi import APIRouter
import sqlite3

router = APIRouter()
DB = "database/cs2.db"

@router.get("/matches")
def get_matches(team: str | None = None):
    c = sqlite3.connect(DB)
    cur = c.cursor()
    if team:
        cur.execute("SELECT * FROM matches WHERE team=?", (team,))
    else:
        cur.execute("SELECT * FROM matches")
    rows = cur.fetchall()
    c.close()
    return rows
