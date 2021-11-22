from sqlmodel import SQLModel


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
