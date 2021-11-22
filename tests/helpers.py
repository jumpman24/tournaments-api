import faker

from app.enums import GameResult
from app.models import Participant, Player, Tournament
from app.schemas import GameCreate, ParticipantCreate, PlayerCreate, TournamentCreate


fake = faker.Faker()


def player_create_data():
    return PlayerCreate(
        last_name=fake.last_name(),
        first_name=fake.first_name(),
        country=fake.country_code(),
        rating=fake.random_int(0, 2700, 5),
    )


def tournament_create_data():
    return TournamentCreate(
        name=f"Tournament of {fake.city()}",
        number_of_rounds=5,
        mm_floor=-20,
        mm_bar=8,
        mm_dense=True,
        handicap_bar=-30,
        handicap_max=9,
        handicap_correction=-2,
    )


def participant_create_data(tournament: Tournament, player: Player, **kwargs):
    return ParticipantCreate(
        tournament_id=tournament.id,
        player_id=player.id,
        rating=player.rating,
        start_mms=0,
        is_final=False,
        **kwargs,
    )


def game_create_data(white: Participant, black: Participant, round_number: int):
    return GameCreate(
        white_id=white.id,
        black_id=black.id,
        round_number=round_number,
        handicap=0,
        result=GameResult.UNKNOWN.value,
        by_default=False,
    )
