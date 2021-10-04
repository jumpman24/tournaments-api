from fastapi import APIRouter, WebSocket

from ..managers import WebSocketManager


router = APIRouter()


@router.websocket("/websocket")
async def websocket_receiver(websocket: WebSocket):
    manager = WebSocketManager(websocket)
    await manager.connect()
    try:
        await manager.run()
    finally:
        await manager.disconnect()
