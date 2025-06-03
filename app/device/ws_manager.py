import asyncio
import json
from app.device.events import event_bus
from fastapi import WebSocket

from app.logger_module.utils import get_logger_factory

get_logger = get_logger_factory(__name__)
logger = get_logger()


class WebWsConnection:
    def __init__(self):
        self.active: dict[int, WebSocket] = {}
        self.pending = {}

    async def add(self, device_id: int, ws: WebSocket):
        self.active[device_id] = ws

    async def remove(self, device_id: int) -> bool:
        try:
            self.active.pop(device_id, None)
            await self.active[device_id].close()
        except Exception as e:
            logger.error(e)
            return False
        return True

    async def get(self, device_id) -> WebSocket | None:
        return self.active.get(device_id)

    async def send_personal(self, device_id: int, data: str | dict) -> dict | None | bool:
        ws = self.active.get(device_id)
        if ws:
            if isinstance(data, dict):
                data = json.dumps(data, ensure_ascii=False)
            await ws.send_text(data)
        else:
            event_bus.emit('message_failed', device_id, data)


class DeviceWsConnection:
    def __init__(self):
        self.active: dict[int, WebSocket] = {}
        self.pending = {}

    async def add(self, device_id: int, ws: WebSocket):
        self.active[device_id] = ws

    async def remove(self, device_id: int) -> bool:
        try:
            self.active.pop(device_id, None)
            await self.active[device_id].close()
        except Exception as e:
            logger.error(e)
            return False
        return True

    async def get(self, device_id) -> WebSocket | None:
        return self.active.get(device_id)

    async def get_list(self):
        return list(self.active.keys())

    async def send_personal(self, device_id: int, data: str | dict,
                            request_id: str = None, timeout: float = 5) -> dict | None | bool:
        ws = self.active.get(device_id)
        if ws:
            if isinstance(data, dict):
                if request_id:
                    data["request_id"] = request_id
                data = json.dumps(data, ensure_ascii=False)
            await ws.send_text(data)

            if request_id:
                future = asyncio.get_event_loop().create_future()
                self.pending.setdefault(device_id, {})[request_id] = future
                try:
                    response = await asyncio.wait_for(future, timeout=timeout)
                    await self.set_response(device_id=device_id, response=response)
                    event_bus.emit('got_reply', device_id, data, str(response))
                    return response
                except asyncio.TimeoutError:
                    event_bus.emit(f'no_reply', device_id, data)
                finally:
                    self.pending[device_id].pop(request_id, None)
            return None
        else:

            event_bus.emit('message_failed', device_id, data)

    async def set_response(self, device_id: int, response: dict | str):
        if isinstance(response, str):
            try:
                response = json.loads(response)
            except Exception as e:
                logger.error(f"Ошибка при разборе сообщения от {device_id}: {e}\n{response}")
                return

        request_id = response.get('request_id', None)
        if request_id and device_id in self.pending and request_id in self.pending[device_id]:
            future = self.pending[device_id][request_id]
            if not future.done():
                future.set_result(response)
        return


device_ws_manager = DeviceWsConnection()
web_ws_manager = WebWsConnection()


@event_bus.on('message_failed')
async def handle_message_failed(device_id, message):
    pass


@event_bus.on('no_reply')
async def handle_no_reply(device_id):
    logger.info(f'[{device_id}]device not replied')
    pass


@event_bus.on('got_reply')
async def handle_got_reply(device_id):
    logger.info(f'[{device_id}]device replied')
