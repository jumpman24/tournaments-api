from pydantic import BaseModel


class WebSocketMessage(BaseModel):
    action: str
    payload: dict
