import json
import random

from app.schemas import PlayerSchema

from .utils import player_create_data


def test_list_players(test_client, players_url, db_players):
    response = test_client.get(players_url)
    assert response.ok
    for item in response.json():
        assert PlayerSchema.validate(item)


def test_create_player(test_client, players_url):
    create_data = json.loads(player_create_data().json())

    response = test_client.post(players_url, json=create_data)
    assert response.ok
    assert PlayerSchema.validate(response.json())


def test_get_player(test_client, players_url, db_players):
    player = random.choice(db_players)
    expected = json.loads(PlayerSchema.from_orm(player).json())

    response = test_client.get(f"{players_url}/{player.id}")
    assert response.ok
    assert response.json() == expected


def test_update_player(test_client, players_url, db_players):
    player = random.choice(db_players)
    not_expected = json.loads(PlayerSchema.from_orm(player).json())

    update_data = json.loads(player_create_data().json())

    response = test_client.put(f"{players_url}/{player.id}", json=update_data)
    assert response.ok
    assert response.json() != not_expected

    response = test_client.get(f"{players_url}/{player.id}")
    assert response.ok
    assert response.json() != not_expected


def test_delete_player(test_client, players_url, db_players):
    player = random.choice(db_players)
    expected = json.loads(PlayerSchema.from_orm(player).json())

    response = test_client.delete(f"{players_url}/{player.id}")
    assert response.ok
    assert response.json() == expected

    response = test_client.get(f"{players_url}/{player.id}")
    assert response.status_code == 404


def test_get_player_history(test_client, players_url, db_session, db_players, db_participants):
    player = random.choice(db_players)
    db_session.refresh(player)

    response = test_client.get(f"{players_url}/{player.id}/history")
    assert response.ok
    assert len(response.json()) == len(player.history)


def test_get_player_not_found(test_client, players_url, db_players):
    fake_id = max(player.id for player in db_players) + 1

    response = test_client.get(f"{players_url}/{fake_id}")
    assert response.status_code == 404


def test_update_player_not_found(test_client, players_url, db_players):
    fake_id = max(player.id for player in db_players) + 1

    update_data = json.loads(player_create_data().json())

    response = test_client.put(f"{players_url}/{fake_id}", json=update_data)
    assert response.status_code == 404


def test_delete_player_not_found(test_client, players_url, db_players):
    fake_id = max(player.id for player in db_players) + 1

    response = test_client.delete(f"{players_url}/{fake_id}")
    assert response.status_code == 404


def test_get_player_history_not_found(test_client, players_url, db_session, db_players, db_participants):
    fake_id = max(player.id for player in db_players) + 1

    response = test_client.get(f"{players_url}/{fake_id}/history")
    assert response.status_code == 404
