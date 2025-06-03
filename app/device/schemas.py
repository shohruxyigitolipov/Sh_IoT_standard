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

    @model_validator(mode="before")
    def convert_state(cls, data):
        # data — dict с исходными данными
        state = data.get('state')
        if isinstance(state, int):
            data['state'] = 'turn_on' if state == 1 else 'turn_off'
        return data


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
