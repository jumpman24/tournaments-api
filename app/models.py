from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


RatingColumnType = Numeric(7, 3)


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)

    last_name = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    rating = Column(RatingColumnType, nullable=False)

    history = relationship("Participant", back_populates="player", cascade="all")

    @property
    def total_tournaments(self) -> int:
        return len(self.history)


class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True)

    name = Column(String(255), nullable=False)
    country = Column(String(2), nullable=False)
    date_start = Column(Date, nullable=False)
    date_end = Column(Date, nullable=False)

    participants = relationship("Participant", back_populates="tournament", cascade="all")

    @property
    def total_participants(self) -> int:
        return len(self.participants)


class Participant(Base):
    __tablename__ = "participants"
    __table_args__ = (UniqueConstraint("player_id", "tournament_id", name="uq_participant"),)

    id = Column(Integer, primary_key=True)
    player_id = Column(ForeignKey("players.id", ondelete="cascade"), nullable=False)
    tournament_id = Column(ForeignKey("tournaments.id", ondelete="cascade"), nullable=False)

    declared_rating = Column(RatingColumnType)
    start_rating = Column(RatingColumnType)
    end_rating = Column(RatingColumnType)

    player = relationship("Player", back_populates="history")
    tournament = relationship("Tournament", back_populates="participants")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
