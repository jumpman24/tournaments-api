from typing import Optional

from sqlmodel import Field, SQLModel


class ParticipantBase(SQLModel):
    player_id: int
    tournament_id: int
    start_mms: int
    absent_rounds: set[int]
    bye_rounds: set[int]
    is_final: bool


class Participant(ParticipantBase, table=True):
    id: Optional[int] = Field(nullable=False, primary_key=True)
    player_id: int = Field(foreign_key="player.id")
    tournament_id: int = Field(foreign_key="tournament.id")


class ParticipantCreate(ParticipantBase):
    start_mms: int = 0
    absent_rounds: set[int] = set()
    bye_rounds: set[int] = set()
    is_final: bool = False


class ParticipantRead(ParticipantBase):
    id: int
