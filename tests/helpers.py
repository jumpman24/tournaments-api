import faker

from app.models.player import PlayerCreate


fake = faker.Faker()


def player_create_data():
    return PlayerCreate(
        last_name=fake.last_name(),
        first_name=fake.first_name(),
        country=fake.country_code(),
        rating=fake.random_int(0, 2700, 5),
    )
