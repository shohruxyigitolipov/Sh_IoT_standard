from typing import Literal
from app.domain.devices.interfaces import IDeviceSender, IDeviceStateManager, IWebSender


class DeviceService:
    def __init__(self, sender: IDeviceSender, sender_web: IWebSender, state_manager: IDeviceStateManager):
        self.sender = sender
        self.sender_web = sender_web
        self.state = state_manager

    async def set_state(self, pin, state: Literal[1, 0]):
        await self.state.set_state(pin=pin, state=state)

    async def set_mode(self, pin, mode: Literal['auto', 'manual']):
        await self.state.set_mode(pin=pin, mode=mode)

    async def set_schedule(self, pin: int, on_time: str, off_time: str):
        await self.state.set_schedule(pin=pin, on_time=on_time, off_time=off_time)

    async def set_name(self, pin: int, name: str):
        await self.state.set_name(pin=pin, name=name)
