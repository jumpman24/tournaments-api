import argparse
from typing import List

from sqlmodel import Session, SQLModel, create_engine

from app.schemas import Game, Participant, Player, Tournament  # noqa: F401
from app.settings import settings
from tests.helpers import (
    participant_create_data,
    player_create_data,
    tournament_create_data,
)


def create_players(db: Session, amount: int = 100) -> List[Player]:
    players = [Player.from_orm(player_create_data()) for _ in range(amount)]
    db.add_all(players)
    db.commit()

    for player in players:
        db.refresh(player)

    return players


def create_tournaments(db: Session, amount: int = 10) -> List[Tournament]:
    tournaments = [Tournament.from_orm(tournament_create_data()) for _ in range(amount)]
    db.add_all(tournaments)
    db.commit()

    for tournament in tournaments:
        db.refresh(tournament)

    return tournaments


def create_participants(
    db: Session, tournaments: list[Tournament], players: list[Player]
) -> List[Participant]:
    participants = [
        Participant.from_orm(participant_create_data(tournament, player))
        for tournament in tournaments
        for player in players
    ]

    db.add_all(participants)
    db.commit()

    for participant in participants:
        db.refresh(participant)

    return participants


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Populate database with mock data")
    parser.add_argument(
        "--database-url",
        type=str,
        help="Database URL",
        default=settings.database_url,
    )
    parser.add_argument("--players", type=int, default=100, help="Number of players")
    parser.add_argument("--tournaments", type=int, default=20, help="Number of players")
    args = parser.parse_args()

    print(f"Target database URL: {args.database_url}")
    answer = input("Proceed? (y/n) > ")

    if answer.lower() not in ["y", "yes"]:
        print("Exiting...")
        exit()

    engine = create_engine(args.database_url)

    print("Dropping database...", end="")
    SQLModel.metadata.drop_all(bind=engine)
    print("OK")
    print("Creating database...", end="")
    SQLModel.metadata.create_all(bind=engine)
    print("OK")

    with Session(engine) as session:
        print("Creating players...", end="")
        db_players = create_players(session, args.players)
        print("OK")
        print("Creating tournaments...", end="")
        db_tournaments = create_tournaments(session, args.tournaments)
        print("OK")
        print("Creating participants...", end="")
        db_participants = create_participants(session, db_tournaments, db_players)
        print("OK")
