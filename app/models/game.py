from typing import Optional

from mcmahon.game import Result
from sqlmodel import Field, SQLModel


class GameBase(SQLModel):
    white_id: int
    black_id: int
    round_number: int
    handicap: int
    result: Result
    by_default: bool


class Game(GameBase, table=True):
    id: Optional[int] = Field(nullable=False, primary_key=True)
    white_id: int = Field(foreign_key="participant.id")
    black_id: int = Field(foreign_key="participant.id")


class GameCreate(GameBase):
    handicap: int = 0
    result: Result = Result.UNKNOWN
    by_default: bool = False


class GameRead(GameBase):
    id: int
