from typing import Dict, cast

from config.config import pins_config, PinMode, PinState
from application.devices.commands import SetMode, SetSchedule
from infrastructure.web_interface.ws_manager import web_ws_manager

from domain.devices.interfaces import IDeviceStateManager


class InMemoryDeviceStateManager(IDeviceStateManager):
    def __init__(self):
        self.pin_modes: Dict[int, PinMode] = {}
        self.pin_state: Dict[int, PinState] = {}
        self.pin_schedule: Dict[int, Dict[str, str]] = {}

        for pin, cfg in pins_config.items():
            self.pin_modes[pin] = cast(PinMode, cfg["mode"])
            self.pin_state[pin] = cast(PinState, cfg["state"])

    async def set_mode(self, pin: int, mode: PinMode):
        self.pin_modes[pin] = mode
        data = SetMode(pin=pin, mode=mode).model_dump()
        await web_ws_manager.send_personal(device_id=1, data=data)

    async def set_state(self, pin: int, state: PinState):
        self.pin_state[pin] = state

    async def set_schedule(self, pin: int, on_time: str, off_time: str):
        self.pin_schedule[pin] = {'on': on_time, 'off': off_time}
        data = SetSchedule(pin=pin, on_time=on_time, off_time=off_time).model_dump()
        await web_ws_manager.send_personal(device_id=1, data=data)

    async def get_mode(self, pin: int) -> PinMode:
        return self.pin_modes.get(pin, PinMode.manual)

    async def get_state(self, pin: int) -> PinState:
        return self.pin_state.get(pin, PinState.OFF)

    async def get_schedule(self, pin: int) -> Dict[str, str]:
        return self.pin_schedule.get(pin, {})
