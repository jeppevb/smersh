import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .schemas import Subject as DtoSubject, Vote as DtoVote, Matchup as DtoMatchup
from .service import get, check_user_exists, vote as register_vote

from ..database import SessionLocal

log = logging.getLogger(__name__)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/",
    response_model=list[DtoSubject],
    summary="Retrieves a list of subjects.",
)
def get_subjects(*, db_session: Session = Depends(get_db)) -> list[DtoSubject]:
    """Retrieves a list of subjects."""
    return get(db_session)


@router.post(
    "/vote",
    response_model=str,
    summary="Votes"
)
def post_vote(vote: DtoVote, db_session: Session = Depends(get_db)):
    assert(check_user_exists(vote.voter, db_session), "User not found")
    register_vote(vote, db_session)
    return "OK"


@router.post(
    "/user",
    response_model=str,
    summary="Creates a user"
)
def post_user(user_name: str, db_session: Session = Depends(get_db)):
    return "OK"

@router.get(
    "/vote",
    response_model=DtoMatchup,
    summary="Retrieves a matchup",
)
def get_subjects(*, db_session: Session = Depends(get_db)) -> list[DtoSubject]:
    """Retrieves a list of subjects."""
    return get(db_session)


