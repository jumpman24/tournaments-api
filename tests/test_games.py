import json
import random

from app.enums import GameResult
from app.schemas.game import GameRead, GameUpdate
from tests.helpers import game_create_data


def test_list_games(test_client, games_url, db_games):
    response = test_client.get(games_url)
    assert response.ok
    for item in response.json():
        assert GameRead.validate(item)


def test_create_game(test_client, games_url, db_tournaments, db_participants):
    tournament = random.choice(db_tournaments)
    white, black = random.sample(
        [p for p in db_participants if p.tournament is tournament], k=2
    )
    create_data = game_create_data(white, black, 0).json()

    response = test_client.post(games_url, data=create_data)
    assert response.ok
    assert GameRead.validate(response.json())


def test_get_game(test_client, games_url, db_games):
    game = random.choice(db_games)
    expected = json.loads(GameRead.from_orm(game).json())

    response = test_client.get(f"{games_url}/{game.id}")
    assert response.ok
    assert response.json() == expected


def test_update_game(test_client, games_url, db_games):
    game = random.choice(db_games)

    update_data = GameUpdate(handicap=2, result=GameResult.WHITE_WINS, by_default=False)

    response = test_client.put(f"{games_url}/{game.id}", data=update_data.json())
    assert response.ok

    expected = GameRead(
        id=game.id,
        white_id=game.white_id,
        black_id=game.black_id,
        round_number=game.round_number,
        **update_data.dict(),
    )
    assert GameRead.parse_raw(response.text) == expected

    response = test_client.get(f"{games_url}/{game.id}")
    assert response.ok
    assert GameRead.parse_raw(response.text) == expected


def test_delete_game(test_client, games_url, db_games):
    game = random.choice(db_games)
    expected = json.loads(GameRead.from_orm(game).json())

    response = test_client.delete(f"{games_url}/{game.id}")
    assert response.ok
    assert response.json() == expected

    response = test_client.get(f"{games_url}/{game.id}")
    assert response.status_code == 404


def test_get_game_not_found(test_client, games_url, db_games):
    fake_id = max(game.id for game in db_games) + 1

    response = test_client.get(f"{games_url}/{fake_id}")
    assert response.status_code == 404


def test_create_game_bad_request(
    test_client, games_url, db_tournaments, db_participants
):
    tournament_1, tournament_2 = random.sample(db_tournaments, k=2)
    white = random.choice([p for p in db_participants if p.tournament is tournament_1])
    black = random.choice(
        [
            participant
            for participant in db_participants
            if participant.tournament == tournament_2
            and participant.player != white.player
        ]
    )

    create_data = game_create_data(white, black, 0).json()

    response = test_client.post(games_url, data=create_data)
    assert response.status_code == 400
    assert (
        response.json()["detail"] == "Participants should play in the same tournament"
    )


def test_create_game_against_themselves(test_client, games_url, db_participants):
    participant = random.choice(db_participants)

    create_data = game_create_data(participant, participant, 0).json()

    response = test_client.post(games_url, data=create_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Participants cannot play against themselves"


def test_create_game_already_played(
    test_client, games_url, db_tournaments, db_games, db_participants
):
    game = random.choice(db_games)
    opponent = random.choice(
        [
            p
            for p in db_participants
            if p != game.white and p.tournament == game.white.tournament
        ]
    )

    create_data = game_create_data(game.white, opponent, game.round_number).json()

    response = test_client.post(games_url, data=create_data)
    assert response.status_code == 400

    expected = "At least one of the participants has the game in the given round"
    assert response.json()["detail"] == expected


def test_update_game_not_found(test_client, games_url, db_games):
    fake_id = max(game.id for game in db_games) + 1

    update_data = GameUpdate(handicap=2, result=GameResult.WHITE_WINS, by_default=False)

    response = test_client.put(f"{games_url}/{fake_id}", data=update_data.json())
    assert response.status_code == 404


def test_delete_game_not_found(test_client, games_url, db_games):
    fake_id = max(game.id for game in db_games) + 1

    response = test_client.delete(f"{games_url}/{fake_id}")
    assert response.status_code == 404
