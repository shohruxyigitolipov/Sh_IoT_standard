from abc import ABC, abstractmethod
from typing import Dict

from app.application.devices.commands import SetMode, SetState, SetSchedule


class IDeviceStateManager(ABC):
    @abstractmethod
    async def set_mode(self, pin, mode): ...

    @abstractmethod
    async def set_state(self, pin, state): ...

    @abstractmethod
    async def set_schedule(self, pin, on_time, off_time): ...

    @abstractmethod
    async def get_mode(self, pin: int) -> str: ...

    @abstractmethod
    async def get_state(self, pin: int) -> int: ...

    @abstractmethod
    async def get_schedule(self, pin: int) -> int: ...


class IDeviceSender(ABC):
    @abstractmethod
    async def send(self, device_id: int, data: dict) -> dict: ...


class IWebSender(ABC):
    @abstractmethod
    async def send(self, device_id: int, data: dict) -> dict: ...
