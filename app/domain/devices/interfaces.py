from abc import ABC, abstractmethod


class IDeviceStateManager(ABC):
    @abstractmethod
    async def set_mode(self, device_id: int, pin, mode): ...

    @abstractmethod
    async def set_state(self, device_id: int, pin, state): ...

    @abstractmethod
    async def set_schedule(self, device_id: int, pin, on_time, off_time): ...

    @abstractmethod
    async def get_mode(self, device_id: int, pin: int) -> str: ...

    @abstractmethod
    async def get_state(self, device_id: int, pin: int) -> int: ...

    @abstractmethod
    async def get_schedule(self, device_id: int, pin: int) -> int: ...

    @abstractmethod
    async def set_name(self, device_id: int, pin: int, name: str): ...

    @abstractmethod
    async def get_name(self, device_id: int, pin: int) -> str: ...



class IDeviceSender(ABC):
    @abstractmethod
    async def send(self, device_id: int, data: dict) -> dict: ...


class IWebSender(ABC):
    @abstractmethod
    async def send(self, device_id: int, data: dict) -> dict: ...
