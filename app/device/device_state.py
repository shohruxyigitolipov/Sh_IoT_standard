from typing import Dict, Literal
from typing import cast

PinMode = Literal["manual", "auto"]
PinState = Literal[1, 0]

DEFAULT_PIN_CONFIG = {
    4: {"mode": "manual", "state": 0},
    5: {"mode": "manual", "state": 0},
    15: {"mode": "manual", "state": 0},
    16: {"mode": "manual", "state": 0},
    17: {"mode": "manual", "state": 0},
    18: {"mode": "manual", "state": 0},
    21: {"mode": "manual", "state": 0},
    22: {"mode": "manual", "state": 0},
    23: {"mode": "manual", "state": 0},
}
const_pings = list(DEFAULT_PIN_CONFIG.keys())


class DeviceStateManager:
    def __init__(self):
        self.pin_modes: Dict[int, PinMode] = {}
        self.pin_status: Dict[int, PinState] = {}
        self.pin_schedule: Dict[int, Dict[str, str]] = {}

        for pin, cfg in DEFAULT_PIN_CONFIG.items():
            self.pin_modes[pin] = cast(PinMode, cfg["mode"])
            self.pin_status[pin] = cast(PinState, cfg["state"])

    def set_mode(self, pin: int, mode: PinMode):
        self.pin_modes[pin] = mode

    def get_mode(self, pin: int) -> PinMode:
        return self.pin_modes.get(pin, "manual")

    def set_status(self, pin: int, state: PinState):
        self.pin_status[pin] = state

    def get_status(self, pin: int) -> PinState:
        return self.pin_status.get(pin, 0)

    def set_schedule(self, pin: int, on_time: str, off_time: str):
        self.pin_schedule[pin] = {"on": on_time, "off": off_time}

    def get_schedule(self, pin: int) -> Dict[str, str]:
        return self.pin_schedule.get(pin, {})

    def export_all_statuses(self) -> Dict[int, PinState]:
        return {pin: self.get_status(pin) for pin in self.pin_status}


device_state = DeviceStateManager()
