from pydantic import BaseModel


class PlayerCreateSchema(BaseModel):
    last_name: str
    first_name: str
    country: str
    rating: float

    class Config:
        schema_extra = {
            "example": {
                "last_name": "Hiliazov",
                "first_name": "Oleksandr",
                "country": "UA",
                "rating": 2269,
            },
        }


class PlayerSchema(BaseModel):
    id: int
    last_name: str
    first_name: str
    country: str
    rating: float

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "last_name": "Hiliazov",
                "first_name": "Oleksandr",
                "country": "UA",
                "rating": 2269,
            },
        }
