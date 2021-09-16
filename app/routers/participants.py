from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..crud import create_instance, delete_instance, get_instance, get_instances, update_instance
from ..dependencies import get_db
from ..models import Participant, Player, Tournament
from ..schemas import ParticipantCreateSchema, ParticipantSchema, ParticipantUpdateSchema


router = APIRouter(tags=["participants"])


@router.get("/participants", response_model=List[ParticipantSchema])
async def get_participants(player_id: int = None, tournament_id: int = None, db: Session = Depends(get_db)):
    filters = []
    if player_id:
        filters.append(Participant.player_id == player_id)
    if tournament_id:
        filters.append(Participant.tournament_id == tournament_id)
    return get_instances(db, Participant, filters)


@router.post("/participants", status_code=201, response_model=ParticipantSchema)
async def create_participant(
    data: ParticipantCreateSchema,
    db: Session = Depends(get_db),
):
    if not get_instance(db, Tournament, data.tournament_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Tournament not found")

    if not get_instance(db, Player, data.player_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Player not found")

    filters = [
        Participant.player_id == data.player_id,
        Participant.tournament_id == data.tournament_id,
    ]
    if get_instances(db, Participant, filters):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Participant already exists")

    return create_instance(db, Participant, data)


@router.get("/participants/{participant_id}", response_model=ParticipantSchema)
async def get_participant(participant_id: int, db: Session = Depends(get_db)):
    if participant := get_instance(db, Participant, participant_id):
        return participant
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.put("/participants/{participant_id}", response_model=ParticipantSchema)
async def update_participant(
    participant_id: int,
    data: ParticipantUpdateSchema,
    db: Session = Depends(get_db),
):
    if participant := update_instance(db, Participant, participant_id, data):
        return participant
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.delete("/participants/{participant_id}", response_model=ParticipantSchema)
async def delete_participant(participant_id: int, db: Session = Depends(get_db)):
    if db_participant := delete_instance(db, Participant, participant_id):
        return db_participant
    raise HTTPException(status.HTTP_404_NOT_FOUND)
