from abc import ABC, abstractmethod


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

    @abstractmethod
    async def set_name(self, pin: int, name: str): ...

    @abstractmethod
    async def get_name(self, pin: int) -> str: ...



class IDeviceSender(ABC):
    @abstractmethod
    async def send(self, device_id: int, data: dict) -> dict: ...


class IWebSender(ABC):
    @abstractmethod
    async def send(self, device_id: int, data: dict) -> dict: ...
