from datetime import datetime

from sqlalchemy import Boolean, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped

from ..database import Base
from ..models import User


class Vote(Base):
    __tablename__ = "votes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    subject_a_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    subject_a: Mapped["Subject"] = relationship("Subject", foreign_keys=subject_a_id)

    subject_b_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    subject_b: Mapped["Subject"] = relationship("Subject", foreign_keys=subject_b_id)

    subject_a_win: Mapped[bool] = mapped_column(Boolean)

    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    voter_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    voter: Mapped["User"] = relationship("User")


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True, unique=True)

    rating: Mapped[int] = mapped_column(Integer, index=True, default=1600)
