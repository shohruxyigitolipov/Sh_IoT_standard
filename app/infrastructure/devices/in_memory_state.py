from typing import Dict, cast

from app.config.config import pins_config, PinMode, PinState
from app.application.devices.commands import SetMode, SetSchedule, SetState
from app.infrastructure.web_interface.ws_manager import web_ws_manager

from app.domain.devices.interfaces import IDeviceStateManager


class InMemoryDeviceStateManager(IDeviceStateManager):
    def __init__(self):
        self.pin_modes: Dict[int, PinMode] = {}
        self.pin_state: Dict[int, PinState] = {}
        self.pin_schedule: Dict[int, Dict[str, str]] = {}

        for pin, cfg in pins_config.items():
            self.pin_modes[pin] = cast(PinMode, cfg["mode"])
            self.pin_state[pin] = cast(PinState, cfg["state"])

    async def set_mode(self, data: SetMode):
        self.pin_modes[data.pin] = data.mode
        await web_ws_manager.send_personal(device_id=1, data=data.model_dump())

    async def set_state(self, data: SetState):
        self.pin_state[data.pin] = data.state

    async def set_schedule(self, data: SetSchedule):
        self.pin_schedule[data.pin] = {'on': data.on_time, 'off': data.off_time}
        await web_ws_manager.send_personal(device_id=1, data=data.model_dump())

    async def get_mode(self, pin: int) -> PinMode:
        return self.pin_modes.get(pin, PinMode.manual)

    async def get_state(self, pin: int) -> PinState:
        return self.pin_state.get(pin, PinState.OFF)

    async def get_schedule(self, pin: int) -> Dict[str, str]:
        return self.pin_schedule.get(pin, {})
