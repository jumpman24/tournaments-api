from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from .enums import GameResult, ScoringStatus


class Player(SQLModel, table=True):
    id: Optional[int] = Field(nullable=False, primary_key=True)
    last_name: str
    first_name: str
    country: str
    rating: int

    participants: List["Participant"] = Relationship(back_populates="player")


class Tournament(SQLModel, table=True):
    id: Optional[int] = Field(nullable=False, primary_key=True)
    name: str
    number_of_rounds: int
    mm_floor: int
    mm_bar: int
    mm_dense: bool
    handicap_bar: int
    handicap_max: int
    handicap_correction: int

    participants: List["Participant"] = Relationship(back_populates="tournament")


class Participant(SQLModel, table=True):
    id: Optional[int] = Field(nullable=False, primary_key=True)
    tournament_id: int = Field(foreign_key="tournament.id")
    player_id: int = Field(foreign_key="player.id")
    rating: int
    start_mms: int
    is_final: bool

    player: Player = Relationship(back_populates="participants")
    tournament: Tournament = Relationship(back_populates="participants")

    rounds: List["Scoring"] = Relationship(back_populates="participant")


class Game(SQLModel, table=True):
    id: Optional[int] = Field(nullable=False, primary_key=True)
    white_id: int = Field(foreign_key="participant.id")
    black_id: int = Field(foreign_key="participant.id")
    round_number: int
    handicap: int
    result: GameResult
    by_default: bool

    white: "Participant" = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Game.white_id"}
    )

    black: "Participant" = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Game.black_id"}
    )


class Scoring(SQLModel, table=True):
    id: Optional[int] = Field(nullable=False, primary_key=True)
    participant_id: Optional[int] = Field(foreign_key="participant.id")
    round_number: int
    status: ScoringStatus = ScoringStatus.UNKNOWN
    points_x2: int = 0
    points_x2_virtual: int = 0

    participant: "Participant" = Relationship(back_populates="rounds")
