
from device.schemas import SetState, SetMode, SetSchedule
from domain.devices.interfaces import IDeviceSender, IDeviceStateManager
from infrastructure.devices.ws_sender import WebSocketWebSender


class DeviceService:
    def __init__(self, sender: IDeviceSender, sender_web: WebSocketWebSender, state_manager: IDeviceStateManager):
        self.sender = sender
        self.sender_web = sender_web
        self.state = state_manager

    async def turn_on(self, device_id: int, pin: int):
        data = SetState(pin=pin, state=1).model_dump()
        response = await self.sender.send(device_id, data)
        if response['result'] == 'ok':
            await self.state.set_state(pin, 1)
            await self.sender_web.send(device_id, data)

    async def turn_off(self, device_id: int, pin: int):
        data = SetState(pin=pin, state=0).model_dump()
        response = await self.sender.send(device_id, data)
        if response['result'] == 'ok':
            await self.state.set_state(pin, 0)
            await self.sender_web.send(device_id, data)

    async def set_state(self, device_id: int, pin: int, state: int):
        data = SetState(pin=pin, state=state).model_dump()
        response = await self.sender.send(device_id, data)
        if response['result'] == 'ok':
            await self.state.set_state(pin, state)
            await self.sender_web.send(device_id=1, data=data)

    async def set_schedule(self, device_id: int, pin: int, on_time: str, off_time: str):
        data = SetSchedule(pin=pin, on_time=on_time, off_time=off_time).model_dump()
        response = await self.sender.send(device_id, data)
        if response['result'] == 'ok':
            await self.state.set_schedule(pin=pin, on_time=on_time, off_time=off_time)
            await self.sender_web.send(device_id, data=data)

    async def set_manual(self, device_id: int, pin: int):
        data = SetMode(pin=pin, mode='manual').model_dump()
        response = await self.sender.send(device_id, data)
        if response['result'] == 'ok':
            await self.state.set_mode(pin=pin, mode='manual')
            await self.sender_web.send(device_id, data)
