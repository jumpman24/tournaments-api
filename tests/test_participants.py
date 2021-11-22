import json
import random

from app.enums import ScoringStatus
from app.schemas import ParticipantRead, ScoringCreate
from app.schemas.participant import ParticipantUpdate
from tests.helpers import participant_create_data


def test_list_participants(
    test_client,
    participants_url,
    db_players,
    db_tournaments,
    db_participants,
):
    tournament = random.choice(db_tournaments)
    player = random.choice(db_players)

    response = test_client.get(
        participants_url, params={"tournament_id": tournament.id}
    )
    assert response.ok
    for item in response.json():
        assert ParticipantRead.validate(item)
        assert item["tournament_id"] == tournament.id

    response = test_client.get(participants_url, params={"player_id": player.id})
    assert response.ok
    for item in response.json():
        assert ParticipantRead.validate(item)
        assert item["player_id"] == player.id

    response = test_client.get(
        participants_url,
        params={"tournament_id": tournament.id, "player_id": player.id},
    )
    assert response.ok
    for item in response.json():
        assert ParticipantRead.validate(item)
        assert item["tournament_id"] == tournament.id
        assert item["player_id"] == player.id


def test_create_participant(test_client, participants_url, db_players, db_tournaments):
    tournament = random.choice(db_tournaments)
    player = random.choice(db_players)

    create_data = participant_create_data(tournament, player).json()

    response = test_client.post(participants_url, data=create_data)
    assert response.ok
    assert ParticipantRead.validate(response.json())


def test_create_participant_with_scoring(
    test_client, participants_url, db_players, db_tournaments
):
    tournament = random.choice(db_tournaments)
    player = random.choice(db_players)

    create_data = participant_create_data(
        tournament,
        player,
        rounds={0: ScoringCreate(round_number=0, status=ScoringStatus.BYE)},
    ).json()

    response = test_client.post(participants_url, data=create_data)
    assert response.ok
    assert ParticipantRead.validate(response.json())


def test_get_participant(test_client, participants_url, db_participants):
    participant = random.choice(db_participants)
    expected = json.loads(ParticipantRead.from_orm(participant).json())

    response = test_client.get(f"{participants_url}/{participant.id}")
    assert response.ok
    assert response.json() == expected


def test_update_participant(test_client, participants_url, db_participants):
    participant = random.choice(db_participants)

    update_data = ParticipantUpdate(rating=777, start_mms=7, is_final=True)
    response = test_client.put(
        f"{participants_url}/{participant.id}", data=update_data.json()
    )
    assert response.ok

    expected = {
        "id": participant.id,
        "player_id": participant.player_id,
        "tournament_id": participant.tournament_id,
        **update_data.dict(),
    }
    assert response.json() == expected

    response = test_client.get(f"{participants_url}/{participant.id}")
    assert response.ok
    assert response.json() == expected


def test_delete_participant(test_client, participants_url, db_participants):
    participant = random.choice(db_participants)
    expected = json.loads(ParticipantRead.from_orm(participant).json())

    response = test_client.delete(f"{participants_url}/{participant.id}")
    assert response.ok
    assert response.json() == expected

    response = test_client.get(f"{participants_url}/{participant.id}")
    assert response.status_code == 404


def test_list_participants_bad_request(
    test_client,
    participants_url,
    db_players,
    db_tournaments,
    db_participants,
):
    response = test_client.get(participants_url)
    assert response.status_code == 400
    assert response.json()["detail"] == "Please provide tournament_id or player_id"


def test_get_participant_not_found(test_client, participants_url, db_participants):
    fake_id = max(participant.id for participant in db_participants) + 1

    response = test_client.get(f"{participants_url}/{fake_id}")
    assert response.status_code == 404


def test_update_participant_not_found(test_client, participants_url, db_participants):
    fake_id = max(participant.id for participant in db_participants) + 1

    update_data = ParticipantUpdate(rating=777, start_mms=7, is_final=True)

    response = test_client.put(f"{participants_url}/{fake_id}", data=update_data.json())
    assert response.status_code == 404


def test_delete_participant_not_found(test_client, participants_url, db_participants):
    fake_id = max(participant.id for participant in db_participants) + 1

    response = test_client.delete(f"{participants_url}/{fake_id}")
    assert response.status_code == 404
