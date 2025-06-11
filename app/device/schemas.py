from pydantic import BaseModel, field_validator, model_validator, Field, TypeAdapter


class PinStateMessage(BaseModel):
    action: str
    pin: int
    state: int

    @field_validator('state')
    def check_state(cls, v):
        if v not in (0, 1):
            raise ValueError('state must be 1 or 0')
        return v


class SetState(BaseModel):
    action: str = 'set_state'
    pin: int
    state: int


class SetMode(BaseModel):
    action: str = 'set_mode'
    pin: int
    mode: str

    @field_validator('mode')
    def check_mode(cls, v):
        if v not in ('manual', 'auto'):
            raise ValueError("mode must be: 'manual' or 'auto'")


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
