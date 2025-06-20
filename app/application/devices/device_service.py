from typing import Literal

from app.application.devices.commands import SetState, SetMode, SetSchedule
from app.config.config import const_pins
from app.domain.devices.interfaces import IDeviceSender, IDeviceStateManager, IWebSender


class DeviceService:
    def __init__(self, sender: IDeviceSender, sender_web: IWebSender, state_manager: IDeviceStateManager):
        self.sender = sender
        self.sender_web = sender_web
        self.state = state_manager

    async def set_state(self, pin, state: Literal[1, 0]):
        data = SetState(pin=pin, state=state)
        await self.state.set_state(data)

    async def set_mode(self, pin, mode: Literal['auto', 'manual']):
        data = SetMode(pin=pin, mode=mode)
        await self.state.set_mode(data)

    async def set_schedule(self, pin: int, on_time: str, off_time: str):
        data = SetSchedule(pin=pin, on_time=on_time, off_time=off_time)
        await self.state.set_schedule(data)


