from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..crud import create_instance
from ..dependencies import get_session
from ..models.tournament import Tournament, TournamentCreate, TournamentRead


router = APIRouter(tags=["players"])


@router.post("/tournaments", response_model=TournamentRead)
def create_tournament(
    data: TournamentCreate,
    session: Session = Depends(get_session),
):
    tournament = create_instance(session, Tournament.from_orm(data))
    return tournament
