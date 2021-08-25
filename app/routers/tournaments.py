from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..crud import create_instance, delete_instance, get_instance, get_instances, update_instance
from ..dependencies import get_db
from ..models import Tournament
from ..schemas import ParticipantSchema, TournamentCreateSchema, TournamentSchema


router = APIRouter(tags=["tournaments"])


@router.get("/tournaments", response_model=List[TournamentSchema])
async def get_tournaments(db: Session = Depends(get_db)):
    return get_instances(db, Tournament)


@router.post("/tournaments", status_code=201, response_model=TournamentSchema)
async def create_tournament(data: TournamentCreateSchema, db: Session = Depends(get_db)):
    return create_instance(db, Tournament, data)


@router.get("/tournaments/{tournament_id}", response_model=TournamentSchema)
async def get_tournament(tournament_id: int, db: Session = Depends(get_db)):
    if tournament := get_instance(db, Tournament, tournament_id):
        return tournament
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.put("/tournaments/{tournament_id}", response_model=TournamentSchema)
async def update_tournament(
    tournament_id: int,
    data: TournamentCreateSchema,
    db: Session = Depends(get_db),
):
    if tournament := update_instance(db, Tournament, tournament_id, data):
        return tournament
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.delete("/tournaments/{tournament_id}", response_model=TournamentSchema)
async def delete_tournament(tournament_id: int, db: Session = Depends(get_db)):
    if db_tournament := delete_instance(db, Tournament, tournament_id):
        return db_tournament
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.get(
    "/tournaments/{tournament_id}/participants",
    response_model=List[ParticipantSchema],
    response_model_exclude={"tournament"},
)
async def get_tournament_participants(
    tournament_id: int,
    db: Session = Depends(get_db),
):
    if tournament := get_instance(db, Tournament, tournament_id):
        return tournament.participants
    raise HTTPException(status.HTTP_404_NOT_FOUND)
