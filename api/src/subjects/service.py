from sqlalchemy import select, insert, update, func, asc, or_
from sqlalchemy.orm import Session
from .models import Subject, Vote, Smersh
from ..models import User
from .schemas import Vote as DtoVote, BaseSubject as CreateSubject, Smersh as CreateSmersh


def get(smersh: str, db_session: Session):
    return db_session.scalars(select(Subject).join(Smersh).where(Smersh.name == smersh)).all()


def calculate_ratings(vote, db_session: Session):
    rating_a = db_session.scalars(select(Subject.rating).where(Subject.name == vote.subject_a)).one()
    rating_b = db_session.scalars(select(Subject.rating).where(Subject.name == vote.subject_b)).one()

    if vote.a_win:
        prob_win = (1.0 / (1.0 + pow(10, ((rating_b - rating_a) / 400))))
    else:
        prob_win = (1.0 / (1.0 + pow(10, ((rating_a - rating_b) / 400))))

    delta_rating = 32 * (1 - prob_win)
    new_a = rating_a + delta_rating * (1 if vote.a_win else -1)
    new_b = rating_b + delta_rating * (-1 if vote.a_win else 1)
    return new_a, new_b


def vote(smersh: str, vote: DtoVote, db_session: Session):
    assert check_subject_exists(vote.subject_a, smersh, db_session), f"Subject {vote.subject_a} does not exist"
    assert check_subject_exists(vote.subject_b, smersh, db_session), f"Subject {vote.subject_b} does not exist"

    db_session.execute(insert(Vote).values(
        [
            {
                "subject_a_id": select(Subject.id).where(
                    Subject.name == vote.subject_a and Subject.smersh_id == select(Smersh.id).where(
                        Smersh.name == vote.smersh)),
                "subject_b_id": select(Subject.id).where(
                    Subject.name == vote.subject_b and Subject.smersh_id == select(Smersh.id).where(
                        Smersh.name == vote.smersh)),
                "voter_id": select(User.id).where(User.name == vote.voter),
                "subject_a_win": vote.a_win
            }
        ]
    ))

    subject_a_new_rating, subject_b_new_rating = calculate_ratings(vote, db_session)

    db_session.execute(update(Subject).where(Subject.name == vote.subject_a).values(rating=subject_a_new_rating))
    db_session.execute(update(Subject).where(Subject.name == vote.subject_b).values(rating=subject_b_new_rating))
    db_session.commit()
    return "OK"


def check_user_exists(voter, db_session: Session):
    return len(db_session.execute(select(User).where(User.name == voter)).all()) > 0


def check_subject_exists(subject, smersh, db_session: Session):
    return len(db_session.execute(select(Subject).where(
        Subject.name == subject and Subject.smersh_id == select(Smersh.id).where(Smersh.name == smersh))).all()) > 0


def create_subject(subject: CreateSubject, db_session: Session):
    db_session.execute(insert(Subject).values(
        [
            {
                "name": subject.name,
                "smersh_id": select(Smersh.id).where(Smersh.name == subject.smersh),
            }
        ]
    ))
    return "OK"


def create_smersh(smersh: CreateSmersh, db_session: Session):
    sm = Smersh(name=smersh.name)
    db_session.add(sm)
    db_session.commit()
    db_session.refresh(sm)
    for sub in smersh.subjects:
        db_session.add(Subject(name=sub, smersh_id=sm.id))
    db_session.commit()
    return "OK"


def get_matchup(smersh: str, db_session: Session):
    var = db_session.scalars(
        select(Subject.name, func.count(Vote.id).label("count"))
            .outerjoin(Vote, onclause=or_(Vote.subject_b_id == Subject.id, Vote.subject_a_id == Subject.id))
            .where(Subject.smersh_id == select(Smersh.id).where(Smersh.name == smersh))
            .group_by("name").order_by('count')).fetchmany(2)
    return var
