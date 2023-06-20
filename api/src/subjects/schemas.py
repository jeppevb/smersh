from datetime import datetime
from pydantic import BaseModel


class Subject(BaseModel):
    name: str
    rating: int


class Vote(BaseModel):
    subject_a: str
    subject_b: str
    timestamp: datetime
    a_win: bool
    voter: str


class Matchup(BaseModel):
    subject_a: str
    subject_b: str