from datetime import datetime
from pydantic import BaseModel


class Subject(BaseModel):
    name: str
    rating: int


class Vote(BaseModel):
    subject_a: Subject
    subject_b: Subject
    timestamp: datetime
    a_win: bool
    voter: str