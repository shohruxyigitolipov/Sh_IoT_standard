from abc import ABC, abstractmethod
from typing import Dict

from application.devices.commands import SetMode, SetState, SetSchedule


class IDeviceStateManager(ABC):
    @abstractmethod
    async def set_mode(self, data: SetMode): ...

    @abstractmethod
    async def set_state(self, data: SetState): ...

    @abstractmethod
    async def set_schedule(self, data: SetSchedule): ...

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
