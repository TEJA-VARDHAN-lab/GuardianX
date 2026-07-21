from pydantic import BaseModel
from typing import Any


class WebSocketEvent(BaseModel):
    event: str
    payload: Any