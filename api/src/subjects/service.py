from sqlalchemy import select, insert, update
from sqlalchemy.orm import Session, aliased
from .models import Subject, Vote
from ..models import User
from .schemas import Vote as DtoVote


def get(db_session: Session):
    return db_session.query(Subject).all()


def calculate_ratings(vote, db_session: Session):
    rating_a = db_session.execute(select(Subject.rating).where(Subject.name == vote.subject_a)).one()[0]
    rating_b = db_session.execute(select(Subject.rating).where(Subject.name == vote.subject_b)).one()[0]

    if vote.a_win:
        prob_win = (1.0 / (1.0 + pow(10, ((rating_b - rating_a) / 400))))
    else:
        prob_win = (1.0 / (1.0 + pow(10, ((rating_a - rating_b) / 400))))

    delta_rating = 32*(1 - prob_win)
    new_a = rating_a + delta_rating * (1 if vote.a_win else -1)
    new_b = rating_b + delta_rating * (-1 if vote.a_win else 1)
    return rating_a, rating_b


def vote(vote: DtoVote, db_session: Session):
    assert check_subject_exists(vote.subject_a, db_session), f"Subject {vote.subject_a} does not exist"
    assert check_subject_exists(vote.subject_b, db_session), f"Subject {vote.subject_b} does not exist"

    db_session.execute(insert(Vote).values(
        [
            {
                "subject_a_id": select(Subject.id).where(Subject.name == vote.subject_a),
                "subject_b_id": select(Subject.id).where(Subject.name == vote.subject_b),
                "voter_id": select(User.id).where(User.name == vote.voter),
                "subject_a_win": vote.a_win
            }
        ]
    ))

    subject_a_new_rating, subject_b_new_rating = calculate_ratings(vote, db_session)

    db_session.execute(update(Subject).where(Subject.name == vote.subject_a).values(rating=subject_a_new_rating))
    db_session.execute(update(Subject).where(Subject.name == vote.subject_b).values(rating=subject_b_new_rating))


def check_user_exists(voter, db_session: Session):
    return len(db_session.execute(select(User).where(User.name == voter)).all()) > 0


def check_subject_exists(subject, db_session: Session):
    return len(db_session.execute(select(Subject).where(Subject.name == subject)).all()) > 0


def create_subject(subject: str, db_session: Session):
    pass