from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ..crud import create_instance, delete_instance, get_instances, update_instance
from ..dependencies import get_session
from ..models.player import Player, PlayerCreate, PlayerRead


router = APIRouter(tags=["players"])


@router.get("/players", response_model=List[PlayerRead])
async def read_players(session: Session = Depends(get_session)):
    return get_instances(session, Player)


@router.post("/players", status_code=201, response_model=PlayerRead)
async def create_player(
    data: PlayerCreate,
    session: Session = Depends(get_session),
):
    player = create_instance(session, Player.from_orm(data))
    return player


@router.get("/players/{player_id}", response_model=PlayerRead)
async def read_player(player_id: int, session: Session = Depends(get_session)):
    if player := session.get(Player, player_id):
        return player
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.put("/players/{player_id}", response_model=PlayerRead)
async def update_player(
    player_id: int, data: PlayerCreate, session: Session = Depends(get_session)
):
    if player := update_instance(session, Player, player_id, data):
        return player
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.delete("/players/{player_id}", response_model=PlayerRead)
async def delete_player(player_id: int, session: Session = Depends(get_session)):
    if player := delete_instance(session, Player, player_id):
        return player
    raise HTTPException(status.HTTP_404_NOT_FOUND)
