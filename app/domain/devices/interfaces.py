from abc import ABC, abstractmethod
from typing import Dict


class IDeviceStateManager(ABC):
    @abstractmethod
    async def set_mode(self, pin: int, mode: str): ...

    @abstractmethod
    async def set_state(self, pin: int, state: int): ...

    @abstractmethod
    async def set_schedule(self, pin: int, on_time: str, off_time: str): ...

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
