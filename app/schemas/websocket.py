from enum import Enum
from typing import Any

from pydantic import BaseModel


class WebSocketAction(str, Enum):
    WHOAMI = "whoami"
    USERS_ADD = "users.add"
    USERS_REMOVE = "users.remove"


class WebSocketMessage(BaseModel):
    action: WebSocketAction
    payload: Any
