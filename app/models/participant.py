from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from .player import Player
    from .tournament import Tournament


class Participant(SQLModel, table=True):
    id: Optional[int] = Field(nullable=False, primary_key=True)
    tournament_id: int = Field(foreign_key="tournament.id")
    player_id: int = Field(foreign_key="player.id")
    rating: int
    start_mms: int
    is_final: bool

    player: "Player" = Relationship(back_populates="participants")
    tournament: "Tournament" = Relationship(back_populates="participants")


class ParticipantCreate(SQLModel):
    tournament_id: int
    player_id: int
    rating: int
    start_mms: int
    is_final: bool

    class Config:
        schema_extra = {
            "example": {
                "player_id": 1,
                "tournament_id": 1,
                "rating": 2100,
                "start_mms": 15,
                "is_final": False,
            }
        }


class ParticipantUpdate(SQLModel):
    rating: int
    start_mms: int
    is_final: bool

    class Config:
        schema_extra = {
            "example": {
                "rating": 2100,
                "start_mms": 15,
                "is_final": False,
            }
        }


class ParticipantRead(SQLModel):
    id: int
    tournament_id: int
    player_id: int
    rating: int
    start_mms: int
    is_final: bool

    class Config:
        schema_extra = {
            "example": {
                "player_id": 1,
                "tournament_id": 1,
                "rating": 2100,
                "start_mms": 15,
                "is_final": False,
            }
        }
