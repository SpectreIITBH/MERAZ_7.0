from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    score = Column(Integer, default=0)
    current_room = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    users = relationship("User", back_populates="team")
    submissions = relationship("FlagSubmission", back_populates="team")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    team_id = Column(Integer, ForeignKey("teams.id"))
    is_admin = Column(Boolean, default=False)

    team = relationship("Team", back_populates="users")

class FlagSubmission(Base):
    __tablename__ = "flag_submissions"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    room_id = Column(Integer)
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_correct = Column(Boolean, default=False)

    team = relationship("Team", back_populates="submissions")
