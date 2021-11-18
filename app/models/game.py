from typing import Optional

from mcmahon.game import Result
from sqlmodel import Field, Relationship, SQLModel

from .participant import Participant


class Game(SQLModel, table=True):
    id: Optional[int] = Field(nullable=False, primary_key=True)
    white_id: int = Field(foreign_key="participant.id")
    black_id: int = Field(foreign_key="participant.id")
    round_number: int
    handicap: int
    result: Result
    by_default: bool

    white: "Participant" = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Game.white_id"}
    )

    black: "Participant" = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Game.black_id"}
    )


class GameCreate(SQLModel):
    white_id: int
    black_id: int
    round_number: int
    handicap: int
    result: Result
    by_default: bool

    class Config:
        schema_extra = {
            "example": {
                "white_id": 1,
                "black_id": 2,
                "round_number": 0,
                "handicap": 0,
                "result": Result.UNKNOWN.value,
                "by_default": False,
            }
        }


class GameUpdate(SQLModel):
    handicap: int
    result: Result
    by_default: bool

    class Config:
        schema_extra = {
            "example": {
                "handicap": 0,
                "result": Result.UNKNOWN.value,
                "by_default": False,
            }
        }


class GameRead(SQLModel):
    id: int
    white_id: int
    black_id: int
    round_number: int
    handicap: int
    result: Result
    by_default: bool

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "white_id": 1,
                "black_id": 2,
                "round_number": 0,
                "handicap": 0,
                "result": Result.WHITE_WINS.value,
                "by_default": False,
            }
        }
