import argparse
from typing import List

from sqlmodel import Session, SQLModel, create_engine

from app.models import Game, Participant, Player, Tournament  # noqa: F401
from app.settings import settings
from tests.helpers import player_create_data


def create_players(db: Session, amount: int = 100) -> List[Player]:
    players = [Player.from_orm(player_create_data()) for _ in range(amount)]
    db.add_all(players)
    db.commit()

    for player in players:
        db.refresh(player)

    return players


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Populate database with mock data")
    parser.add_argument(
        "--database-url",
        type=str,
        help="Database URL",
        default=settings.database_url,
    )
    parser.add_argument("--players", type=int, default=100, help="Number of players")
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
