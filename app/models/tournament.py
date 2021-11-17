from typing import Optional

from sqlmodel import Field, SQLModel


class TournamentBase(SQLModel):
    name: str
    number_of_rounds: int
    mm_floor: int
    mm_bar: int
    mm_dense: bool
    handicap_bar: int
    handicap_max: int
    handicap_correction: int


class Tournament(TournamentBase, table=True):
    id: Optional[int] = Field(nullable=False, primary_key=True)


class TournamentCreate(TournamentBase):
    number_of_rounds: int = 5
    mm_floor: int = -20
    mm_bar: int = 8
    mm_dense: bool = True
    handicap_bar: int = -30
    handicap_max: int = 9
    handicap_correction: int = 0


class TournamentRead(TournamentBase):
    id: int
