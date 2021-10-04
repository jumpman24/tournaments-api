import json
import random

from app.schemas import TournamentSchema
from utils.mock_data import tournament_create_data


def test_list_tournaments(test_client, tournaments_url, db_tournaments):
    response = test_client.get(tournaments_url)
    assert response.ok


def test_create_tournament(test_client, tournaments_url):
    create_data = tournament_create_data().json()
    response = test_client.post(tournaments_url, data=create_data)
    assert response.ok
    assert TournamentSchema.validate(response.json())


def test_get_tournament(test_client, tournaments_url, db_tournaments):
    tournament = random.choice(db_tournaments)
    expected = json.loads(TournamentSchema.from_orm(tournament).json())

    response = test_client.get(f"{tournaments_url}/{tournament.id}")
    assert response.ok
    assert response.json() == expected


def test_update_tournament(test_client, tournaments_url, db_tournaments):
    tournament = random.choice(db_tournaments)
    not_expected = json.loads(TournamentSchema.from_orm(tournament).json())

    update_data = tournament_create_data().json()

    response = test_client.put(f"{tournaments_url}/{tournament.id}", data=update_data)
    assert response.ok
    assert response.json() != not_expected

    response = test_client.get(f"{tournaments_url}/{tournament.id}")
    assert response.ok
    assert response.json() != not_expected


def test_delete_tournament(test_client, tournaments_url, db_tournaments):
    tournament = random.choice(db_tournaments)
    expected = json.loads(TournamentSchema.from_orm(tournament).json())

    response = test_client.delete(f"{tournaments_url}/{tournament.id}")
    assert response.ok
    assert response.json() == expected

    response = test_client.get(f"{tournaments_url}/{tournament.id}")
    assert response.status_code == 404


def test_get_tournament_participants(test_client, tournaments_url, db_tournaments, db_participants):
    tournament = random.choice(db_tournaments)

    response = test_client.get(f"{tournaments_url}/{tournament.id}/participants")
    assert response.ok
    assert len(response.json()) == len(tournament.participants)


def test_get_tournament_not_found(test_client, tournaments_url, db_tournaments):
    fake_id = max(player.id for player in db_tournaments) + 1

    response = test_client.get(f"{tournaments_url}/{fake_id}")
    assert response.status_code == 404


def test_update_tournament_not_found(test_client, tournaments_url, db_tournaments):
    fake_id = max(player.id for player in db_tournaments) + 1
    update_data = tournament_create_data().json()

    response = test_client.put(f"{tournaments_url}/{fake_id}", data=update_data)
    assert response.status_code == 404


def test_delete_tournament_not_found(test_client, tournaments_url, db_tournaments):
    fake_id = max(player.id for player in db_tournaments) + 1

    response = test_client.delete(f"{tournaments_url}/{fake_id}")
    assert response.status_code == 404


def test_get_tournament_participants_not_found(test_client, tournaments_url, db_tournaments, db_participants):
    fake_id = max(player.id for player in db_tournaments) + 1

    response = test_client.get(f"{tournaments_url}/{fake_id}/participants")
    assert response.status_code == 404
