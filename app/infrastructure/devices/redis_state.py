import json
from dataclasses import dataclass, field
from typing import Dict, Literal

from redis.asyncio import Redis

from app.config import (
    pins_config,
    const_pins,
    PinMode,
    PinState,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
)
from app.domain.devices.interfaces import IDeviceStateManager


@dataclass
class DeviceState:
    pin_modes: Dict[int, PinMode] = field(default_factory=dict)
    pin_state: Dict[int, PinState] = field(default_factory=dict)
    pin_schedule: Dict[int, Dict[str, str]] = field(default_factory=dict)
    pin_names: Dict[int, str] = field(default_factory=dict)


class RedisDeviceStateManager(IDeviceStateManager):
    def __init__(self):
        self.redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
        self.devices: Dict[int, DeviceState] = {}

    async def preload(self):
        keys = await self.redis.keys("device:*")
        for key in keys:
            raw = await self.redis.get(key)
            if not raw:
                continue
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                continue
            device_id = int(key.split(":")[1])
            self.devices[device_id] = self._state_from_report(data)

    async def save_report(self, device_id: int, report: dict):
        await self.redis.set(f"device:{device_id}", json.dumps(report))

    async def _get_device(self, device_id: int) -> DeviceState:
        if device_id not in self.devices:
            self.devices[device_id] = self._create_default_state()
        return self.devices[device_id]

    @staticmethod
    def _state_from_report(data: dict) -> DeviceState:
        state = DeviceState()
        for pin in data.get("pin_list", []):
            p = pin.get("pin")
            if p is None:
                continue
            state.pin_modes[p] = pin.get("mode")
            state.pin_state[p] = pin.get("state")
            state.pin_schedule[p] = pin.get("schedule", {})
            name = pin.get("name")
            if name is not None:
                state.pin_names[p] = name
        return state

    @staticmethod
    def _create_default_state() -> DeviceState:
        state = DeviceState()
        for pin, cfg in pins_config.items():
            state.pin_modes[pin] = cfg["mode"]
            state.pin_state[pin] = cfg["state"]
        for pin in const_pins:
            state.pin_schedule[pin] = {"on_time": "12:00", "off_time": "13:00"}
        return state

    async def set_mode(self, device_id: int, pin, mode):
        device = await self._get_device(device_id)
        device.pin_modes[pin] = mode

    async def set_state(self, device_id: int, pin, state):
        device = await self._get_device(device_id)
        device.pin_state[pin] = state

    async def set_schedule(self, device_id: int, pin, on_time, off_time):
        device = await self._get_device(device_id)
        device.pin_schedule[pin] = {"on_time": on_time, "off_time": off_time}

    async def set_name(self, device_id: int, pin: int, name: str | None):
        device = await self._get_device(device_id)
        if name is not None:
            device.pin_names[pin] = name
        else:
            device.pin_names.pop(pin, None)

    async def get_name(self, device_id: int, pin: int) -> str | None:
        device = await self._get_device(device_id)
        return device.pin_names.get(pin)

    async def get_mode(self, device_id: int, pin: int) -> Literal["manual", "auto"] | None:
        device = await self._get_device(device_id)
        return device.pin_modes.get(pin)

    async def get_state(self, device_id: int, pin: int) -> PinState:
        device = await self._get_device(device_id)
        return device.pin_state.get(pin)

    async def get_schedule(self, device_id: int, pin: int) -> Dict[str, str]:
        device = await self._get_device(device_id)
        return device.pin_schedule.get(pin, {})

    async def get_report(self, device_id: int, pin: int | None = None):
        device = await self._get_device(device_id)
        if not pin:
            pin_list = list(const_pins)
        else:
            pin_list = [pin]
        report_data = []
        for p in pin_list:
            data = {
                "pin": p,
                "state": await self.get_state(device_id, p),
                "mode": await self.get_mode(device_id, p),
                "schedule": await self.get_schedule(device_id, p),
                "name": await self.get_name(device_id, p),
            }
            report_data.append(data)
        payload = {"type": "report", "pin_list": report_data}
        return payload


device_state = RedisDeviceStateManager()

