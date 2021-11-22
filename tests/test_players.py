import json
import random

from app.schemas.player import PlayerRead
from tests.helpers import player_create_data


def test_list_players(test_client, players_url, db_players):
    response = test_client.get(players_url)
    assert response.ok
    for item in response.json():
        assert PlayerRead.validate(item)


def test_create_player(test_client, players_url):
    create_data = player_create_data().json()

    response = test_client.post(players_url, data=create_data)
    assert response.ok
    assert PlayerRead.validate(response.json())


def test_get_player(test_client, players_url, db_players):
    player = random.choice(db_players)
    expected = json.loads(PlayerRead.from_orm(player).json())

    response = test_client.get(f"{players_url}/{player.id}")
    assert response.ok
    assert response.json() == expected


def test_update_player(test_client, players_url, db_players):
    player = random.choice(db_players)
    not_expected = json.loads(PlayerRead.from_orm(player).json())

    update_data = player_create_data().json()

    response = test_client.put(f"{players_url}/{player.id}", data=update_data)
    assert response.ok
    assert response.json() != not_expected

    response = test_client.get(f"{players_url}/{player.id}")
    assert response.ok
    assert response.json() != not_expected


def test_delete_player(test_client, players_url, db_players):
    player = random.choice(db_players)
    expected = json.loads(PlayerRead.from_orm(player).json())

    response = test_client.delete(f"{players_url}/{player.id}")
    assert response.ok
    assert response.json() == expected

    response = test_client.get(f"{players_url}/{player.id}")
    assert response.status_code == 404


def test_get_player_not_found(test_client, players_url, db_players):
    fake_id = max(player.id for player in db_players) + 1

    response = test_client.get(f"{players_url}/{fake_id}")
    assert response.status_code == 404


def test_update_player_not_found(test_client, players_url, db_players):
    fake_id = max(player.id for player in db_players) + 1

    update_data = player_create_data().json()

    response = test_client.put(f"{players_url}/{fake_id}", data=update_data)
    assert response.status_code == 404


def test_delete_player_not_found(test_client, players_url, db_players):
    fake_id = max(player.id for player in db_players) + 1

    response = test_client.delete(f"{players_url}/{fake_id}")
    assert response.status_code == 404
