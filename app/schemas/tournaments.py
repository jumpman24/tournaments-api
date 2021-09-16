from datetime import date

from pydantic import BaseModel


class TournamentCreateSchema(BaseModel):
    name: str
    country: str
    date_start: date
    date_end: date

    class Config:
        schema_extra = {
            "example": {
                "name": "Championship of Ukraine 2021 - semifinals",
                "country": "UA",
                "date_start": "2021-09-04",
                "date_end": "2021-09-05",
            },
        }


class TournamentSchema(BaseModel):
    id: int
    name: str
    country: str
    date_start: date
    date_end: date
    total_participants: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Championship of Ukraine 2021",
                "country": "UA",
                "date_start": "2021-01-01",
                "date_end": "2021-01-02",
                "total_participants": 16,
            },
        }
