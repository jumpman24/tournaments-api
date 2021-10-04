import asyncio
from collections import defaultdict
from typing import Dict, List

from fastapi import WebSocket

from ..schemas.websocket import WebSocketMessage


class WebSocketManager:
    connections: Dict[str, List[WebSocket]] = defaultdict(list)

    def __init__(self, websocket: WebSocket):
        self.websocket = websocket

    async def connect(self):
        await self.websocket.accept()

    async def disconnect(self):
        for room, websockets in self.connections.items():
            if websockets.remove(self.websocket):
                await self.broadcast(room, {"action": "users.disconnect", "payload": "user-data"})

    def join_room(self, room: str):
        self.connections[room].append(self.websocket)

    def leave_room(self, room: str):
        self.connections[room].remove(self.websocket)

    async def broadcast(self, room: str, message: dict):
        tasks = [websocket.send_json(message) for websocket in self.connections[room]]
        await asyncio.gather(*tasks)

    async def run(self):
        async for message in self.websocket.iter_json():
            data = WebSocketMessage.parse_obj(message)
            await self.websocket.send_json({"action": "echo", "payload": data.payload})
