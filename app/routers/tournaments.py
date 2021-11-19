from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ..crud import delete_instance, insert_instance, select_instances, update_instance
from ..dependencies import get_session
from ..models import ParticipantRead
from ..models.tournament import Tournament, TournamentCreate, TournamentRead


router = APIRouter(tags=["tournaments"])


@router.get("/tournaments", response_model=list[TournamentRead])
async def read_tournaments(session: Session = Depends(get_session)):
    tournaments = select_instances(session, Tournament)
    return tournaments


@router.post("/tournaments", response_model=TournamentRead)
def create_tournament(
    data: TournamentCreate,
    session: Session = Depends(get_session),
):
    tournament = insert_instance(session, Tournament.from_orm(data))
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


@router.get(
    "/tournaments/{tournament_id}/participants", response_model=list[ParticipantRead]
)
async def read_tournament_participants(
    tournament_id: int,
    session: Session = Depends(get_session),
):
    if tournament := session.get(Tournament, tournament_id):
        return tournament.participants
    raise HTTPException(status.HTTP_404_NOT_FOUND)
