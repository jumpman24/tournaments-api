from typing import Optional

from sqlmodel import Field, SQLModel


class Participant(SQLModel, table=True):
    id: Optional[int] = Field(nullable=False, primary_key=True)
    tournament_id: int = Field(foreign_key="tournament.id")
    player_id: int = Field(foreign_key="player.id")
    rating: int
    start_mms: int
    is_final: bool


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
