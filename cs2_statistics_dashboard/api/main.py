from fastapi import FastAPI
from api.routers import auth, teams, matches
from database.db import init_db, seed_admin, seed_matches, seed_teams

init_db()
seed_admin()
seed_matches()
seed_teams()

app = FastAPI(title="CS2 API")

app.include_router(auth.router)
app.include_router(teams.router)
app.include_router(matches.router)
