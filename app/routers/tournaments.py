from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ..crud import create_instance, delete_instance, get_instances, update_instance
from ..dependencies import get_session
from ..models.tournament import Tournament, TournamentCreate, TournamentRead


router = APIRouter(tags=["tournaments"])


@router.get("/tournaments", response_model=List[TournamentRead])
async def read_tournaments(session: Session = Depends(get_session)):
    return get_instances(session, Tournament)


@router.post("/tournaments", response_model=TournamentRead)
def create_tournament(
    data: TournamentCreate,
    session: Session = Depends(get_session),
):
    tournament = create_instance(session, Tournament.from_orm(data))
    return tournament


@router.get("/tournaments/{tournament_id}", response_model=TournamentRead)
async def read_tournament(tournament_id: int, session: Session = Depends(get_session)):
    if tournament := session.get(Tournament, tournament_id):
        return tournament
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.put("/tournaments/{tournament_id}", response_model=TournamentRead)
async def update_tournament(
    tournament_id: int,
    data: TournamentCreate,
    session: Session = Depends(get_session),
):
    if tournament := update_instance(session, Tournament, tournament_id, data):
        return tournament
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.delete("/tournaments/{tournament_id}", response_model=TournamentRead)
async def delete_tournament(
    tournament_id: int, session: Session = Depends(get_session)
):
    if tournament := delete_instance(session, Tournament, tournament_id):
        return tournament
    raise HTTPException(status.HTTP_404_NOT_FOUND)
