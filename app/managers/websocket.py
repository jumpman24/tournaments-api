import asyncio
from typing import AsyncIterator, Set

from fastapi import WebSocket
from pydantic import ValidationError

from ..loggers import logger
from ..models import User
from ..schemas import WebSocketMessage


class Connection:
    def __init__(self, websocket: WebSocket, user: User):
        self.websocket = websocket
        self.user = user

    def __str__(self):
        return str(self.websocket.client)

    async def accept(self):
        return await self.websocket.accept()

    async def send_text(self, message: str):
        await self.websocket.send_text(message)

    def iter_text(self) -> AsyncIterator[str]:
        return self.websocket.iter_text()


class WebSocketManager:
    websockets: Set[Connection] = set()

    def __init__(self, websocket: WebSocket, user: User):
        self.websocket = Connection(websocket, user)

    async def connect(self):
        await self.websocket.accept()
        self.websockets.add(self.websocket)
        logger.info(f"{self} connected")

    def disconnect(self):
        self.websockets.remove(self.websocket)
        logger.info(f"{self} disconnected")

    async def send_personal_message(self, message: WebSocketMessage):
        await self.websocket.send_text(message.json())

    async def iter_message(self) -> AsyncIterator[WebSocketMessage]:
        async for data in self.websocket.iter_text():
            try:
                yield WebSocketMessage.parse_raw(data)
            except ValidationError:
                pass

    @staticmethod
    async def send_message(websocket: Connection, message: WebSocketMessage):
        await websocket.send_text(message.json())

    @classmethod
    async def broadcast(cls, message: WebSocketMessage):
        tasks = [cls.send_message(websocket, message) for websocket in cls.websockets]
        await asyncio.gather(*tasks)

    def users_online(self) -> Set[User]:
        return {websocket.user for websocket in self.websockets if websocket.user}
