from dataclasses import dataclass, field
from typing import Dict, cast, Literal

from app.config import pins_config, PinMode, PinState, const_pins
from app.domain.devices.interfaces import IDeviceStateManager


@dataclass
class DeviceState:
    pin_modes: Dict[int, PinMode] = field(default_factory=dict)
    pin_state: Dict[int, PinState] = field(default_factory=dict)
    pin_schedule: Dict[int, Dict[str, str]] = field(default_factory=dict)
    pin_names: Dict[int, str] = field(default_factory=dict)


class InMemoryDeviceStateManager(IDeviceStateManager):
    def __init__(self):
        self.devices: Dict[int, DeviceState] = {}

    def _get_device(self, device_id: int) -> DeviceState:
        if device_id not in self.devices:
            state = DeviceState()
            for pin, cfg in pins_config.items():
                state.pin_modes[pin] = cast(PinMode, cfg["mode"])
                state.pin_state[pin] = cast(PinState, cfg["state"])
            for pin in const_pins:
                state.pin_schedule[pin] = {'on_time': '12:00', 'off_time': '13:00'}
            self.devices[device_id] = state
        return self.devices[device_id]

    async def set_mode(self, device_id: int, pin: int, mode):
        device = self._get_device(device_id)
        device.pin_modes[pin] = mode

    async def set_state(self, device_id: int, pin: int, state):
        device = self._get_device(device_id)
        device.pin_state[pin] = state

    async def set_schedule(self, device_id: int, pin: int, on_time: str, off_time: str):
        device = self._get_device(device_id)
        device.pin_schedule[pin] = {'on_time': on_time, 'off_time': off_time}

    async def set_name(self, device_id: int, pin: int, name: str):
        device = self._get_device(device_id)
        device.pin_names[pin] = name

    async def get_name(self, device_id: int, pin: int) -> str | None:
        device = self._get_device(device_id)
        return device.pin_names.get(pin)

    async def get_mode(self, device_id: int, pin: int) -> Literal["manual", "auto"] | None:
        device = self._get_device(device_id)
        return device.pin_modes.get(pin)

    async def get_state(self, device_id: int, pin: int) -> PinState:
        device = self._get_device(device_id)
        return device.pin_state.get(pin)

    async def get_schedule(self, device_id: int, pin: int) -> Dict[str, str]:
        device = self._get_device(device_id)
        return device.pin_schedule.get(pin, {})

    async def get_report(self, device_id: int, pin: int | None = None):
        device = self._get_device(device_id)
        if not pin:
            pin_list = list(const_pins)
        else:
            pin_list = [pin]
        report_data = []
        for pin in pin_list:
            data = {
                'pin': pin,
                'state': await self.get_state(device_id, pin),
                'mode': await self.get_mode(device_id, pin),
                'schedule': await self.get_schedule(device_id, pin=pin),
                'name': await self.get_name(device_id, pin)
            }

            report_data.append(data)
        payload = {'type': 'report', 'pin_list': report_data}
        return payload


device_state = InMemoryDeviceStateManager()
