from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..crud import create_instance, delete_instance, get_instance, get_instances, update_instance
from ..dependencies import get_db
from ..models import Player
from ..schemas import ParticipantSchema, PlayerCreateSchema, PlayerSchema


router = APIRouter(tags=["players"])


@router.get("/players", response_model=List[PlayerSchema])
async def get_players(db: Session = Depends(get_db)):
    return get_instances(db, Player)


@router.post("/players", status_code=201, response_model=PlayerSchema)
async def create_player(data: PlayerCreateSchema, db: Session = Depends(get_db)):
    return create_instance(db, Player, data)


@router.get("/players/{player_id}", response_model=PlayerSchema)
async def get_player(player_id: int, db: Session = Depends(get_db)):
    if player := get_instance(db, Player, player_id):
        return player
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.put("/players/{player_id}", response_model=PlayerSchema)
async def update_player(player_id: int, data: PlayerCreateSchema, db: Session = Depends(get_db)):
    if player := update_instance(db, Player, player_id, data):
        return player
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.delete("/players/{player_id}", response_model=PlayerSchema)
async def delete_player(player_id: int, db: Session = Depends(get_db)):
    if db_player := delete_instance(db, Player, player_id):
        return db_player
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.get(
    "/players/{player_id}/history",
    response_model=List[ParticipantSchema],
    response_model_exclude={"player"},
)
async def get_player_history(player_id: int, db: Session = Depends(get_db)):
    if player := get_instance(db, Player, player_id):
        return player.history
    raise HTTPException(status.HTTP_404_NOT_FOUND)
