from typing import Literal

from application.devices.commands import SetState, SetMode, SetSchedule
from domain.devices.interfaces import IDeviceSender, IDeviceStateManager
from infrastructure.web_interface.ws_sender import WebSocketWebSender


class DeviceService:
    def __init__(self, sender: IDeviceSender, sender_web: WebSocketWebSender, state_manager: IDeviceStateManager):
        self.sender = sender
        self.sender_web = sender_web
        self.state = state_manager

    @staticmethod
    def _is_success(response: dict) -> bool:
        return response.get('result') == 'ok'

    async def turn_on(self, device_id: int, pin):
        data = SetState(pin=pin, state=1)
        response = await self.sender.send(device_id, data.model_dump())
        if self._is_success(response):
            await self.state.set_state(data=data)
            await self.sender_web.send(device_id, data.model_dump())

    async def turn_off(self, device_id: int, pin):
        data = SetState(pin=pin, state=0)
        response = await self.sender.send(device_id, data.model_dump())
        if self._is_success(response):
            await self.state.set_state(data=data)
            await self.sender_web.send(device_id, data.model_dump())

    async def set_state(self, device_id: int, pin, state: Literal[1, 0]):
        data = SetState(pin=pin, state=state)
        response = await self.sender.send(device_id=device_id, data=data.model_dump())
        if self._is_success(response):
            await self.state.set_state(data=data)
            await self.sender_web.send(device_id=device_id, data=data.model_dump())

    async def set_schedule(self, device_id: int, pin: int, on_time: str, off_time: str):
        data = SetSchedule(pin=pin, on_time=on_time, off_time=off_time)
        response = await self.sender.send(device_id=device_id, data=data.model_dump())
        if self._is_success(response):
            await self.state.set_schedule(data=data)
            await self.sender_web.send(device_id=device_id, data=data.model_dump())

    async def set_manual(self, device_id: int, pin: int):
        data = SetMode(pin=pin, mode='manual')
        response = await self.sender.send(device_id=device_id, data=data.model_dump())
        if self._is_success(response):
            await self.state.set_mode(data=data)
            await self.sender_web.send(device_id=device_id, data=data.model_dump())
