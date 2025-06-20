from typing import Dict, cast, Literal

from app.application.devices.commands import SetMode, SetSchedule, SetState
from app.config.config import pins_config, PinMode, PinState, const_pins
from app.domain.devices.interfaces import IDeviceStateManager


class InMemoryDeviceStateManager(IDeviceStateManager):
    def __init__(self):
        self.pin_modes: Dict[int, PinMode] = {}
        self.pin_state: Dict[int, PinState] = {}
        self.pin_schedule: Dict[int, Dict[str, str]] = {}

        for pin, cfg in pins_config.items():
            self.pin_modes[pin] = cast(PinMode, cfg["mode"])
            self.pin_state[pin] = cast(PinState, cfg["state"])
        for pin in const_pins:
            self.pin_schedule[pin] = {'on_time': '12:00', 'off_time': '13:00'}

    async def set_mode(self, pin, mode):
        self.pin_modes[pin] = mode

    async def set_state(self, pin, state):
        self.pin_state[pin] = state

    async def set_schedule(self, pin, on_time, off_time):
        self.pin_schedule[pin] = {'on_time': on_time, 'off_time': off_time}

    async def get_mode(self, pin) -> Literal["manual", "auto"] | None:
        return self.pin_modes.get(pin)

    async def get_state(self, pin: int) -> PinState:
        return self.pin_state.get(pin)

    async def get_schedule(self, pin: int) -> Dict[str, str]:
        return self.pin_schedule.get(pin, {})

    async def get_report(self, pin: int = None):
        if not pin:
            pin_list = []
            for pin in const_pins:
                pin_list.append(pin)
        else:
            pin_list = [pin]
        report_data = []
        for pin in pin_list:
            data = {'pin': pin,
                    'state': await self.get_state(pin),
                    'mode': await self.get_mode(pin),
                    'schedule': await self.get_schedule(pin=pin)}
            report_data.append(data)
        payload = {'type': 'report', 'pin_list': report_data}
        return payload


device_state = InMemoryDeviceStateManager()
