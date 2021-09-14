import json
import random

import faker

from app.schemas import ParticipantSchema
from utils.mock_data import participant_create_data, participant_update_data


fake = faker.Faker()


def test_list_participants(test_client, participants_url, db_participants):
    response = test_client.get(participants_url)
    assert response.ok
    for item in response.json():
        assert ParticipantSchema.validate(item)


def test_filter_participants_by_player(test_client, participants_url, db_players, db_participants):
    player = random.choice(db_players)
    response = test_client.get(participants_url, params={"player_id": player.id})
    assert response.ok
    assert len(response.json()) == len(player.history)


def test_filter_participants_by_tournament(test_client, participants_url, db_tournaments, db_participants):
    tournament = random.choice(db_tournaments)
    response = test_client.get(participants_url, params={"tournament_id": tournament.id})
    assert response.ok
    assert len(response.json()) == len(tournament.participants)


def test_create_participant(test_client, db_players, db_tournaments, participants_url):
    player = random.choice(db_players)
    tournament = random.choice(db_tournaments)
    create_data = json.loads(participant_create_data(player.id, tournament.id).json())

    response = test_client.post(participants_url, json=create_data)
    assert response.ok
    assert ParticipantSchema.validate(response.json())


def test_get_participant(test_client, db_participants, participants_url):
    participant = random.choice(db_participants)
    expected = json.loads(ParticipantSchema.from_orm(participant).json())

    response = test_client.get(f"{participants_url}/{participant.id}")
    assert response.ok
    assert response.json() == expected


def test_update_participant(test_client, db_participants, participants_url):
    participant = random.choice(db_participants)
    not_expected = ParticipantSchema.from_orm(participant)
    update_data = json.loads(participant_update_data().json())

    response = test_client.put(f"{participants_url}/{participant.id}", json=update_data)
    assert response.ok
    assert response.json() != not_expected

    response = test_client.get(f"{participants_url}/{participant.id}")
    assert response.ok
    assert response.json() != not_expected


def test_delete_participant(test_client, db_session, db_participants, participants_url):
    participant = random.choice(db_participants)
    expected = json.loads(ParticipantSchema.from_orm(participant).json())

    response = test_client.delete(f"{participants_url}/{participant.id}")
    assert response.ok
    assert response.json() == expected

    response = test_client.get(f"{participants_url}/{participant.id}")
    assert response.status_code == 404


def test_create_participant_player_not_found(test_client, db_players, db_tournaments, participants_url):
    fake_player_id = max(player.id for player in db_players) + 1
    tournament = random.choice(db_tournaments)
    create_data = json.loads(participant_create_data(fake_player_id, tournament.id).json())

    response = test_client.post(participants_url, json=create_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Player not found"


def test_create_participant_tournament_not_found(test_client, db_players, db_tournaments, participants_url):
    player = random.choice(db_players)
    fake_tournament_id = max(tournament.id for tournament in db_tournaments) + 1
    create_data = json.loads(participant_create_data(player.id, fake_tournament_id).json())

    response = test_client.post(participants_url, json=create_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Tournament not found"


def test_get_participant_not_found(test_client, db_participants, participants_url):
    fake_id = max(participant.id for participant in db_participants) + 1

    response = test_client.get(f"{participants_url}/{fake_id}")
    assert response.status_code == 404


def test_update_participant_not_found(test_client, db_participants, participants_url):
    fake_id = max(participant.id for participant in db_participants) + 1
    update_data = json.loads(participant_update_data().json())

    response = test_client.put(f"{participants_url}/{fake_id}", json=update_data)
    assert response.status_code == 404


def test_delete_participant_not_found(test_client, db_session, db_participants, participants_url):
    fake_id = max(participant.id for participant in db_participants) + 1

    response = test_client.delete(f"{participants_url}/{fake_id}")
    assert response.status_code == 404
