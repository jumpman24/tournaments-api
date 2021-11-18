from typing import Optional

from sqlmodel import Field, SQLModel


class Participant(SQLModel, table=True):
    id: Optional[int] = Field(nullable=False, primary_key=True)
    player_id: int = Field(foreign_key="player.id")
    tournament_id: int = Field(foreign_key="tournament.id")
    rating: int
    start_mms: int
    is_final: bool


class ParticipantCreate(SQLModel):
    player_id: int
    tournament_id: int
    rating: int
    start_mms: int
    is_final: bool


class ParticipantUpdate(SQLModel):
    rating: int
    start_mms: int
    is_final: bool


class ParticipantRead(SQLModel):
    id: int
    player_id: int
    tournament_id: int
    rating: int
    start_mms: int
    is_final: bool
