from typing import Optional

from fastapi import APIRouter, Depends, WebSocket

from ..dependencies import get_current_user_websocket
from ..managers import WebSocketManager
from ..models import User
from ..schemas import UserSchema, WebSocketMessage


router = APIRouter()


def whoami_message(user: Optional[User] = None):
    return WebSocketMessage(action="whoami", payload=UserSchema.from_orm(user) if user else None)


def users_add_message(user: User):
    return WebSocketMessage(action="users.add", payload=UserSchema.from_orm(user))


def users_remove_message(user: User):
    return WebSocketMessage(action="users.remove", payload=UserSchema.from_orm(user))


@router.websocket("/websocket")
async def websocket_receiver(websocket: WebSocket, current_user: Optional[User] = Depends(get_current_user_websocket)):
    manager = WebSocketManager(websocket, current_user)
    await manager.connect()
    await manager.send_personal_message(whoami_message(current_user))

    for user in manager.users_online():
        if user != current_user:
            await manager.send_personal_message(users_add_message(user))

    if current_user:
        await manager.broadcast(users_add_message(current_user))

    try:
        async for message in manager.iter_message():
            await manager.send_personal_message(message)
    finally:
        manager.disconnect()

        if current_user:
            await manager.broadcast(users_remove_message(current_user))
