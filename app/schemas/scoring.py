from sqlmodel import SQLModel

from ..enums import ScoringStatus


class ScoringCreate(SQLModel):
    round_number: int
    status: ScoringStatus = ScoringStatus.UNKNOWN
    points_x2: int = 0
    points_x2_virtual: int = 0

    class Config:
        schema_extra = {
            "example": {
                "round_number": 0,
                "status": ScoringStatus.UNKNOWN.value,
                "points_x2": 0,
                "points_x2_virtual": 0,
            }
        }


class ScoringUpdate(SQLModel):
    status: ScoringStatus
    points_x2: int
    points_x2_virtual: int

    class Config:
        schema_extra = {
            "example": {
                "status": ScoringStatus.BYE.value,
                "points_x2": 2,
                "points_x2_virtual": 2,
            }
        }


class ScoringRead(SQLModel):
    id: int
    participant_id: int
    round_number: int
    status: ScoringStatus
    points_x2: int
    points_x2_virtual: int

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "participant_id": 1,
                "round_number": 0,
                "status": ScoringStatus.PAIRED.value,
                "points_x2": 2,
                "points_x2_virtual": 2,
            }
        }
