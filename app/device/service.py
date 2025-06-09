import uuid
from abc import ABC, abstractmethod
from typing import Dict
from typing import cast

from app.device.ws_manager import device_ws_manager, web_ws_manager
from config import pins_config, PinState, PinMode
from device.schemas import SetState, SetMode, SetSchedule


class DeviceStateManager:
    def __init__(self):
        self.pin_modes: Dict[int, PinMode] = {}
        self.pin_status: Dict[int, PinState] = {}
        self.pin_schedule: Dict[int, Dict[str, str]] = {}

        for pin, cfg in pins_config.items():
            self.pin_modes[pin] = cast(PinMode, cfg["mode"])
            self.pin_status[pin] = cast(PinState, cfg["state"])

    async def set_mode(self, pin: int, mode: PinMode):
        self.pin_modes[pin] = mode
        data = SetMode(pin=pin, mode=mode).model_dump()
        await web_ws_manager.send_personal(device_id=1, data=data)

    async def set_state(self, pin: int, state: PinState):
        self.pin_status[pin] = state
        data = SetState(pin=pin, state=state).model_dump()
        await web_ws_manager.send_personal(device_id=1, data=data)

    async def set_schedule(self, pin: int, on_time: str, off_time: str):
        self.pin_schedule[pin] = {"on": on_time, "off": off_time}
        data = SetSchedule(pin=pin, on_time=on_time, off_time=off_time).model_dump()
        await web_ws_manager.send_personal(device_id=1, data=data)

    async def get_mode(self, pin: int) -> PinMode:
        return self.pin_modes.get(pin, "manual")

    async def get_status(self, pin: int) -> PinState:
        return self.pin_status.get(pin, 0)

    async def get_schedule(self, pin: int) -> Dict[str, str]:
        return self.pin_schedule.get(pin, {})


device_state = DeviceStateManager()


class BaseDevice(ABC):
    def __init__(self, device_id: int):
        self.device_id = device_id

    async def send_data_ws(self, data: dict) -> dict:
        """
        Отправка данных устройству через WebSocket.
        :param data: JSON-словарь команды.
        """
        request_id = str(uuid.uuid4())
        response = await device_ws_manager.send_personal(device_id=self.device_id, data=data, timeout=30,
                                                         request_id=request_id)
        print(f'Websocket device answer: {response}')
        return response

    @abstractmethod
    async def turn_on(self, pin: int) -> None:
        pass

    @abstractmethod
    async def turn_off(self, pin: int) -> None:
        pass

    @abstractmethod
    async def set_state(self, pin: int, state: bool) -> None:
        pass

    @abstractmethod
    async def set_schedule(self, pin: int, on_time: str, off_time: str) -> None:
        pass

    @abstractmethod
    async def set_manual(self, pin: int):
        pass


class DeviceCommands(BaseDevice):
    async def turn_on(self, pin: int) -> None:
        data = SetState(pin=pin, state=1).model_dump()
        response = await self.send_data_ws(data)
        if response['result'] == 'ok':
            await device_state.set_state(pin, 1)

    async def turn_off(self, pin: int) -> None:
        data = SetState(pin=pin, state=0).model_dump()
        response = await self.send_data_ws(data)
        if response['result'] == 'ok':
            await device_state.set_state(pin=pin, state=0)

    async def set_state(self, pin: int, state: int) -> None:
        data = SetState(pin=pin, state=state).model_dump()
        response = await self.send_data_ws(data)
        if response['result'] == 'ok':
            await device_state.set_state(pin=pin, state=state)

    async def set_schedule(self, pin: int, on_time: str, off_time: str) -> None:
        data = SetSchedule(pin=pin, on_time=on_time, off_time=off_time).model_dump()
        response = await self.send_data_ws(data)
        if response['result'] == 'ok':
            await device_state.set_schedule(pin=pin, on_time=on_time, off_time=off_time)

    async def set_manual(self, pin: int) -> None:
        data = SetMode(pin=pin, mode='manual').model_dump()
        response = await self.send_data_ws(data)
        if response['result'] == 'ok':
            await device_state.set_mode(pin=pin, mode='manual')
            await device_state.set_state(pin=pin, state=0)
