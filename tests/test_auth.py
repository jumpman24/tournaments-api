import random

from app.schemas import UserSchema
from utils.mock_data import user_create_data


def test_sign_up(test_client, base_url):
    post_data = user_create_data().json()
    response = test_client.post(f"{base_url}/sign-up", data=post_data)
    assert response.ok
    assert UserSchema.validate(response.json())


def test_sign_in(test_client, base_url, db_users):
    user = random.choice(db_users)
    user_data = {"username": user.username, "password": "password"}
    response = test_client.post(f"{base_url}/sign-in", data=user_data)
    assert response.ok
    assert "access_token" in response.json()


def test_whoami(test_client, base_url, db_users):
    user = random.choice(db_users)
    user_data = {"username": user.username, "password": "password"}
    response = test_client.post(f"{base_url}/sign-in", data=user_data)
    assert response.ok
    token = response.json()["access_token"]

    response = test_client.get(
        f"{base_url}/whoami",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.ok
    assert response.json() == UserSchema.from_orm(user)
