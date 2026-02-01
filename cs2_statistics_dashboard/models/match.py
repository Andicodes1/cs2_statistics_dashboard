from pydantic import BaseModel

class Match(BaseModel):
    id: int | None = None
    date: str
    team: str
    opponent: str
    map: str
    result: str
    event: str
