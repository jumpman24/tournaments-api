from typing import Optional

from sqlmodel import Field, SQLModel


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


class TournamentCreate(SQLModel):
    name: str
    number_of_rounds: int
    mm_floor: int
    mm_bar: int
    mm_dense: bool
    handicap_bar: int
    handicap_max: int
    handicap_correction: int

    class Config:
        schema_extra = {
            "example": {
                "name": "Championship of Ukraine 2021 - quarterfinals",
                "number_of_rounds": 5,
                "mm_floor": -20,
                "mm_bar": 8,
                "mm_dense": True,
                "handicap_bar": -30,
                "handicap_max": 9,
                "handicap_correction": -2,
            }
        }


class TournamentRead(SQLModel):
    id: int
    name: str
    number_of_rounds: int
    mm_floor: int
    mm_bar: int
    mm_dense: bool
    handicap_bar: int
    handicap_max: int
    handicap_correction: int

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Championship of Ukraine 2021 - quarterfinals",
                "number_of_rounds": 5,
                "mm_floor": -20,
                "mm_bar": 8,
                "mm_dense": True,
                "handicap_bar": -30,
                "handicap_max": 9,
                "handicap_correction": -2,
            }
        }
