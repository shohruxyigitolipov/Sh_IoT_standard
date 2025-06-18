from typing import Literal
from app.config.config import const_pins
from pydantic import BaseModel, field_validator


class PinStateMessage(BaseModel):
    action: str
    pin: int
    state: Literal[1, 0]


class SetState(BaseModel):
    action: str = 'set_state'
    pin: Literal[4, 5, 16, 17, 18, 21, 22, 23]
    state: Literal[1, 0]


class SetMode(BaseModel):
    action: str = 'set_mode'
    pin: int
    mode: Literal["manual", "auto"]


class SetSchedule(BaseModel):
    action: str = 'set_schedule'
    pin: int
    on_time: str
    off_time: str


class DeviceMessageBase(BaseModel):
    action: str


class PingMessage(BaseModel):
    action: str
    timestamp: int


class StateUpdateMessage(BaseModel):
    action: str
    pin: int
    state: str


def parse_message(data: dict):
    action = data.get("action")
    if action == "ping":
        return PingMessage(**data)
    elif action == "set_state":
        return StateUpdateMessage(**data)
    elif action == 'set_mode':
        pass
    elif action == 'set_manual':
        pass
    elif action == 'result':
        pass
    elif action == 'set_state':
        pass
    else:
        raise ValueError("Unknown message type")
