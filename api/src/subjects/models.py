from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)

    rating = Column(Integer, index=True, default=1600)
    
    votes = relationship("Vote")


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    
    subject_a_id = Column(Integer, ForeignKey("subjects.id"))
    subject_a = relationship("Subject", back_populates="votes")
    
    subject_b_id = Column(Integer, ForeignKey("subjects.id"))
    subject_b = relationship("Subject", back_populates="votes")

    subject_a_win = Column(Boolean)
    
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    voter_id = Column(Integer, ForeignKey("users.id"))
    voter = relationship("User", back_populates="votes")