from typing import Optional

from sqlmodel import Field, SQLModel


class Player(SQLModel, table=True):
    id: Optional[int] = Field(nullable=False, primary_key=True)
    last_name: str
    first_name: str
    country: str
    rating: int


class PlayerCreate(SQLModel):
    last_name: str
    first_name: str
    country: str
    rating: int = 100

    class Config:
        schema_extra = {
            "example": {
                "last_name": "Doe",
                "first_name": "John",
                "country": "US",
                "rating": 2100,
            }
        }


class PlayerRead(SQLModel):
    id: int
    last_name: str
    first_name: str
    country: str
    rating: int

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "last_name": "Doe",
                "first_name": "John",
                "country": "US",
                "rating": 2100,
            }
        }
