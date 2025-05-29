import uuid

from abc import ABC, abstractmethod
from typing import Optional

from app.device.device_state import device_state
from app.ws.manager import ws_manager


class BaseDevice(ABC):
    def __init__(self, device_id: int):
        self.device_id = device_id

    async def send_data_ws(self, data: dict) -> None:
        """
        Отправка данных устройству через WebSocket.
        :param data: JSON-словарь команды.
        """
        request_id = str(uuid.uuid4())
        response = await ws_manager.send_personal(device_id=self.device_id, data=data, timeout=30,
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

    @abstractmethod
    async def get_status(self, pin: int) -> Optional[bool]:
        pass


class DeviceCommands(BaseDevice):
    async def turn_on(self, pin: int) -> None:
        device_state.set_state(pin, 'on')
        return await self.send_data_ws({
            "action": "turn_on",
            "pin": pin,
        })

    async def turn_off(self, pin: int) -> None:
        device_state.set_status(pin, 'off')
        return await self.send_data_ws({
            "action": "turn_off",
            "pin": pin,
        })

    async def set_state(self, pin: int, state: int) -> None:
        device_state.set_status(pin, state)
        return await self.send_data_ws({
            "action": "set_state",
            "pin": pin,
            "state": state
        })

    async def set_schedule(self, pin: int, on_time: str, off_time: str) -> None:
        device_state.set_schedule(pin, on_time, off_time)
        device_state.set_mode(pin, 'auto')
        return await self.send_data_ws({
            "action": "set_schedule",
            "pin": pin,
            "on_time": on_time,
            "off_time": off_time
        })

    async def set_manual(self, pin: int) -> None:
        device_state.set_mode(pin, 'manual')
        return await self.send_data_ws({
            "action": "set_manual",
            "pin": pin,
        })

    async def get_status(self, pin: int):
        """
        Запрос состояния устройства.
        :return: Ожидаемое состояние (если сервер отвечает).
        """
        return await self.send_data_ws({
            "action": "get_status",
            "pin": pin,
        })
