from datetime import timedelta

import faker

from app.schemas import (
    ParticipantCreateSchema,
    ParticipantUpdateSchema,
    PlayerCreateSchema,
    TournamentCreateSchema,
    UserCreateSchema,
)


fake = faker.Faker()


def player_create_data():
    return PlayerCreateSchema(
        last_name=fake.last_name(),
        first_name=fake.first_name(),
        country=fake.country_code(),
        rating=fake.random_int(0, 2700, 5),
    )


def tournament_create_data():
    date_start = fake.date_between()
    date_end = date_start + timedelta(days=1)

    return TournamentCreateSchema(
        name=f"Championship of {fake.city()}",
        country=fake.country_code(),
        date_start=date_start,
        date_end=date_end,
    )


def participant_create_data(player_id: int, tournament_id: int):
    return ParticipantCreateSchema(
        player_id=player_id,
        tournament_id=tournament_id,
        declared_rating=fake.random_int(100, 2700, 5),
    )


def participant_update_data():
    return ParticipantUpdateSchema(
        declared_rating=fake.random_int(100, 2700, 5),
    )


def user_create_data():
    return UserCreateSchema(
        username=fake.user_name(),
        full_name=fake.name(),
        password="password",
    )
