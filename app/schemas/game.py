from sqlmodel import SQLModel

from ..enums import GameResult


class GameCreate(SQLModel):
    white_id: int
    black_id: int
    round_number: int
    handicap: int
    result: GameResult
    by_default: bool

    class Config:
        schema_extra = {
            "example": {
                "white_id": 1,
                "black_id": 2,
                "round_number": 0,
                "handicap": 0,
                "result": GameResult.UNKNOWN.value,
                "by_default": False,
            }
        }


class GameUpdate(SQLModel):
    handicap: int
    result: GameResult
    by_default: bool

    class Config:
        schema_extra = {
            "example": {
                "handicap": 0,
                "result": GameResult.UNKNOWN.value,
                "by_default": False,
            }
        }


class GameRead(SQLModel):
    id: int
    white_id: int
    black_id: int
    round_number: int
    handicap: int
    result: GameResult
    by_default: bool

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "white_id": 1,
                "black_id": 2,
                "round_number": 0,
                "handicap": 0,
                "result": GameResult.WHITE_WINS.value,
                "by_default": False,
            }
        }
