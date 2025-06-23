from typing import Literal
from app.domain.devices.interfaces import IDeviceSender, IDeviceStateManager, IWebSender


class DeviceService:
    def __init__(self, sender: IDeviceSender, sender_web: IWebSender, state_manager: IDeviceStateManager):
        self.sender = sender
        self.sender_web = sender_web
        self.state = state_manager

    async def set_state(self, device_id: int, pin, state: Literal[1, 0]):
        await self.state.set_state(device_id, pin=pin, state=state)

    async def set_mode(self, device_id: int, pin, mode: Literal['auto', 'manual']):
        await self.state.set_mode(device_id, pin=pin, mode=mode)

    async def set_schedule(self, device_id: int, pin: int, on_time: str, off_time: str):
        await self.state.set_schedule(device_id, pin=pin, on_time=on_time, off_time=off_time)

    async def set_name(self, device_id: int, pin: int, name: str):
        await self.state.set_name(device_id, pin=pin, name=name)
