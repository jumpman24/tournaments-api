from typing import Dict

from sqlmodel import SQLModel

from app.schemas.scoring import ScoringCreate


class ParticipantCreate(SQLModel):
    tournament_id: int
    player_id: int
    rating: int
    start_mms: int
    is_final: bool

    rounds: Dict[int, ScoringCreate] = {}

    class Config:
        schema_extra = {
            "example": {
                "player_id": 1,
                "tournament_id": 1,
                "rating": 2100,
                "start_mms": 15,
                "is_final": False,
                "rounds": [ScoringCreate.Config.schema_extra["example"]],
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
