from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ..crud import create_instance, delete_instance, get_instances, update_instance
from ..dependencies import get_session
from ..models.participant import (
    Participant,
    ParticipantCreate,
    ParticipantRead,
    ParticipantUpdate,
)


router = APIRouter(tags=["tournaments"])


@router.get("/participants", response_model=List[ParticipantRead])
async def read_participants(
    tournament_id: int = None,
    player_id: int = None,
    session: Session = Depends(get_session),
):
    filters = []
    if tournament_id:
        filters.append(Participant.tournament_id == tournament_id)
    if player_id:
        filters.append(Participant.player_id == player_id)
    return get_instances(session, Participant, filters=filters)


@router.post("/participants", response_model=ParticipantRead)
def create_participant(
    data: ParticipantCreate,
    session: Session = Depends(get_session),
):
    tournament = create_instance(session, Participant.from_orm(data))
    return tournament


@router.get("/participants/{participant_id}", response_model=ParticipantRead)
async def read_participant(
    participant_id: int, session: Session = Depends(get_session)
):
    if participant := session.get(Participant, participant_id):
        return participant
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.put("/participants/{participant_id}", response_model=ParticipantRead)
async def update_participant(
    participant_id: int,
    data: ParticipantUpdate,
    session: Session = Depends(get_session),
):
    if participant := update_instance(session, Participant, participant_id, data):
        return participant
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.delete("/participants/{participant_id}", response_model=ParticipantRead)
async def delete_participant(
    participant_id: int, session: Session = Depends(get_session)
):
    if participant := delete_instance(session, Participant, participant_id):
        return participant
    raise HTTPException(status.HTTP_404_NOT_FOUND)
