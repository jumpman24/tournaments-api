from pydantic import BaseModel, PositiveFloat

from .players import PlayerSchema
from .tournaments import TournamentSchema


class ParticipantCreateSchema(BaseModel):
    player_id: int
    tournament_id: int
    declared_rating: PositiveFloat

    class Config:
        schema_extra = {
            "example": {
                "player_id": 1,
                "tournament_id": 1,
                "declared_rating": 2200,
            }
        }


class ParticipantUpdateSchema(BaseModel):
    declared_rating: PositiveFloat

    class Config:
        schema_extra = {"example": {"declared_rating": 2200}}


class ParticipantSchema(BaseModel):
    id: int
    player_id: int
    tournament_id: int
    declared_rating: PositiveFloat = None
    start_rating: PositiveFloat = None
    end_rating: PositiveFloat = None

    player: PlayerSchema
    tournament: TournamentSchema

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "player_id": 1,
                "tournament_id": 1,
                "declared_rating": 2200,
                "start_rating": 2248,
                "end_rating": 2269,
                "player": PlayerSchema.Config.schema_extra["example"],
                "tournament": TournamentSchema.Config.schema_extra["example"],
            }
        }
