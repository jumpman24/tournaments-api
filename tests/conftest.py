from typing import List

import faker
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.dependencies import get_session
from app.main import app
from app.models import Participant, Player, Tournament
from app.settings import settings
from tests.helpers import (
    participant_create_data,
    player_create_data,
    tournament_create_data,
)


if settings.test_database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}

engine = create_engine(settings.test_database_url, connect_args=connect_args)

SQLModel.metadata.drop_all(bind=engine)
SQLModel.metadata.create_all(bind=engine)

fake = faker.Faker()


def override_get_db():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_db


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def db_session() -> Session:
    with Session(engine) as session:
        yield session


@pytest.fixture
def db_players(db_session) -> List[Player]:
    players = [Player.from_orm(player_create_data()) for _ in range(16)]
    db_session.add_all(players)
    db_session.commit()

    for player in players:
        db_session.refresh(player)

    return players


@pytest.fixture
def db_tournaments(db_session) -> List[Tournament]:
    tournaments = [Tournament.from_orm(tournament_create_data()) for _ in range(3)]
    db_session.add_all(tournaments)
    db_session.commit()

    for tournament in tournaments:
        db_session.refresh(tournament)

    return tournaments


@pytest.fixture
def db_participants(db_session, db_players, db_tournaments) -> List[Participant]:
    participants = []

    for tournament in db_tournaments:
        for player in db_players:
            participants.append(
                Participant.from_orm(participant_create_data(tournament, player))
            )

    db_session.add_all(participants)
    db_session.commit()

    for participant in participants:
        db_session.refresh(participant)

    return participants


@pytest.fixture
def players_url() -> str:
    return "/api/v1/players"


@pytest.fixture
def tournaments_url() -> str:
    return "/api/v1/tournaments"


@pytest.fixture
def participants_url() -> str:
    return "/api/v1/participants"
