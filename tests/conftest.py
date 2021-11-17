from typing import List

import faker
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.dependencies import get_session
from app.main import app
from app.models.player import Player
from app.settings import settings
from tests.helpers import player_create_data


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
    players = [Player(**player_create_data().dict()) for _ in range(3)]
    db_session.add_all(players)
    db_session.commit()

    for player in players:
        db_session.refresh(player)

    yield players

    for player in players:
        db_session.delete(player)

    db_session.commit()


@pytest.fixture
def players_url() -> str:
    return "/api/v1/players"
