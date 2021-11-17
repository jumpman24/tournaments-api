import argparse
import random
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, create_session

from app.database import Base
from app.models import Participant, Player, Tournament, User
from app.settings import settings
from utils.mock_data import (
    participant_create_data,
    player_create_data,
    tournament_create_data,
    user_create_data,
)


def create_users(db: Session, amount: int = 100) -> List[User]:
    users = [User(**user_create_data().dict()) for _ in range(amount)]
    db.add_all(users)
    db.commit()

    for user in users:
        db.refresh(user)

    return users


def create_players(db: Session, amount: int = 100) -> List[Player]:
    players = [Player(**player_create_data().dict()) for _ in range(amount)]
    db.add_all(players)
    db.commit()

    for player in players:
        db.refresh(player)

    return players


def create_tournaments(db: Session, amount: int = 30) -> List[Tournament]:
    tournaments = [Tournament(**tournament_create_data().dict()) for _ in range(amount)]
    db.add_all(tournaments)
    db.commit()

    for tournament in tournaments:
        db.refresh(tournament)

    return tournaments


def create_participants(
    db: Session,
    players: List[Player],
    tournaments: List[Tournament],
    amount: int = 16,
) -> List[Participant]:
    participants = [
        Participant(**participant_create_data(player.id, tournament.id).dict())
        for player in random.sample(players, amount)
        for tournament in tournaments
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
    parser.add_argument("--users", type=int, default=10, help="Number of users")
    parser.add_argument("--players", type=int, default=100, help="Number of players")
    parser.add_argument(
        "--tournaments", type=int, default=30, help="Number of tournaments"
    )
    parser.add_argument(
        "--participants",
        type=int,
        default=16,
        help="Number of participants per tournament",
    )
    args = parser.parse_args()

    print(f"Target database URL: {args.database_url}")
    answer = input("Proceed? (y/n) > ")

    if answer.lower() not in ["y", "yes"]:
        print("Exiting...")
        exit()

    engine = create_engine(args.database_url)
    session = create_session(
        engine, autoflush=True, future=True, expire_on_commit=False
    )

    print("Dropping database...", end="")
    Base.metadata.drop_all(bind=engine)
    print("OK\nCreating database...", end="")
    Base.metadata.create_all(bind=engine)
    print("OK\nCreating users...", end="")
    db_users = create_users(session, args.users)
    print("OK\nCreating players...", end="")
    db_players = create_players(session, args.players)
    print("OK\nCreating tournaments...", end="")
    db_tournaments = create_tournaments(session, args.tournaments)
    print("OK\nCreating participants...", end="")
    participants = create_participants(
        session, db_players, db_tournaments, args.participants
    )
    print("OK")
