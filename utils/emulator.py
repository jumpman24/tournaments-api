import asyncio
import random
from typing import List

import websockets

from app.auth import create_token
from app.database import SessionLocal
from app.managers import DatabaseManager
from app.models import User
from app.schemas import WebSocketMessage


NUM_USERS = 100
NUM_GUESTS = 1

MAX_USERNAME_LENGTH = 0
MAX_ACTION_LENGTH = 0


def format_message(username: str, action: str, payload):
    global MAX_USERNAME_LENGTH, MAX_ACTION_LENGTH
    MAX_ACTION_LENGTH = max(MAX_ACTION_LENGTH, len(action))
    MAX_USERNAME_LENGTH = max(MAX_USERNAME_LENGTH, len(username))
    print(f"{username:{MAX_USERNAME_LENGTH}s} [{action:{MAX_ACTION_LENGTH}s}] {payload}")


async def connect_websocket(url_path, username, token: str = None):
    if token:
        url_path += f"?token={token}"
    while True:
        await asyncio.sleep(1)
        try:
            websocket = await websockets.connect(url_path)

            while True:
                message = WebSocketMessage.parse_raw(await websocket.recv())
                format_message(username, message.action, message.payload)
        except Exception as exc:
            format_message(username, exc.__class__.__name__, str(exc))


async def run():
    session = SessionLocal()
    try:
        db = DatabaseManager(session)
        all_users: List[User] = db.get_instances(User)
    finally:
        session.close()

    users = random.sample(all_users, min(5, len(all_users)))
    tokens = {user.username: create_token(user.id) for user in users}
    tokens.update({f"guest__{i}": None for i in range(NUM_GUESTS)})

    while True:
        await asyncio.gather(
            *[connect_websocket("ws://localhost:8000/websocket", username, token) for username, token in tokens.items()]
        )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run())
