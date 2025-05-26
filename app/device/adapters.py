import uuid

from abc import ABC, abstractmethod
from typing import Optional

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
    async def turn_on(self) -> None:
        pass

    @abstractmethod
    async def turn_off(self) -> None:
        pass

    @abstractmethod
    async def set_state(self, state: bool) -> None:
        pass

    @abstractmethod
    async def set_timer(self, start_time: str, stop_time: str) -> None:
        pass

    @abstractmethod
    async def get_status(self) -> Optional[bool]:
        pass


class DeviceCommands(BaseDevice):
    async def turn_on(self) -> None:
        return await self.send_data_ws({
            "action": "turn_on"
        })

    async def turn_off(self) -> None:
        return await self.send_data_ws({
            "action": "turn_off"
        })

    async def set_state(self, state: bool) -> None:
        return await self.send_data_ws({
            "action": "set_state",
            "state": state
        })

    async def set_timer(self, start_time: str, stop_time: str) -> None:
        return await self.send_data_ws({
            "action": "set_timer",
            "start_time": start_time,
            "stop_time": stop_time
        })

    async def clear_timer(self) -> None:
        return await self.send_data_ws({
            "action": "clear_timer"
        })

    async def get_status(self):
        """
        Запрос состояния устройства.
        :return: Ожидаемое состояние (если сервер отвечает).
        """
        return await self.send_data_ws({
            "action": "get_status"
        })
