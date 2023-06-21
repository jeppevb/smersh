from datetime import datetime
from pydantic import BaseModel


class BaseSubject(BaseModel):
    name: str
    smersh: str


class Subject(BaseSubject):
    rating: int


class Smersh(BaseModel):
    subjects: list[str]
    name: str


class Vote(BaseModel):
    subject_a: str
    subject_b: str
    timestamp: datetime
    a_win: bool
    voter: str


class Matchup(BaseModel):
    subject_a: str
    subject_b: str