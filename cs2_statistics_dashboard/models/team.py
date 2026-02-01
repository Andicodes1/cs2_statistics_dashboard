from pydantic import BaseModel

class Team(BaseModel):
    id: int | None = None
    name: str
    logo_url: str
