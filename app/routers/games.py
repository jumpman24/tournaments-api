from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, or_

from ..crud import delete_instance, insert_instance, select_instances, update_instance
from ..dependencies import get_session
from ..models import Game, GameCreate, GameRead, GameUpdate, Participant


router = APIRouter(tags=["games"])


@router.get("/games", response_model=list[GameRead])
async def read_games(session: Session = Depends(get_session)):
    games = select_instances(session, Game)
    return games


@router.post("/games", response_model=GameRead)
def create_game(data: GameCreate, session: Session = Depends(get_session)):
    white = session.get(Participant, data.white_id)
    black = session.get(Participant, data.black_id)

    if white.player_id == black.player_id:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Participants cannot play against themselves",
        )

    if white.tournament_id != black.tournament_id:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Participants should play in the same tournament",
        )

    filters = [
        Game.round_number == data.round_number,
        or_(
            Game.white_id == data.white_id,
            Game.white_id == data.black_id,
            Game.black_id == data.white_id,
            Game.black_id == data.black_id,
        ),
    ]
    if select_instances(session, Game, filters=filters):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "At least one of the participants has the game in the given round",
        )
    game = insert_instance(session, Game.from_orm(data))
    return game


@router.get("/games/{game_id}", response_model=GameRead)
async def read_game(game_id: int, session: Session = Depends(get_session)):
    if game := session.get(Game, game_id):
        return game
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.put("/games/{game_id}", response_model=GameRead)
async def update_game(
    game_id: int,
    data: GameUpdate,
    session: Session = Depends(get_session),
):
    if game := update_instance(session, Game, game_id, data):
        return game
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.delete("/games/{game_id}", response_model=GameRead)
async def delete_game(game_id: int, session: Session = Depends(get_session)):
    if game := delete_instance(session, Game, game_id):
        return game
    raise HTTPException(status.HTTP_404_NOT_FOUND)
