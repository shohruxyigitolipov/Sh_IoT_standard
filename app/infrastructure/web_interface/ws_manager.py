from fastapi import WebSocket

from app.config import event_bus
from app.infrastructure.logger_module.utils import get_logger_factory

get_logger = get_logger_factory(__name__)
logger = get_logger()


class WebClientWebSocketManager:
    def __init__(self):
        self.active: dict[int, WebSocket] = {}

    async def add(self, device_id: int, ws: WebSocket):
        self.active[device_id] = ws
        event_bus.emit('web_ws_connected', device_id, ws)

    async def remove(self, device_id: int):
        try:
            event_bus.emit('web_ws_disconnected', device_id)
            await self.active.pop(device_id, None).close()
        except:
            pass

    async def send_personal(self, device_id: int, data: str | dict):
        ws = self.active.get(device_id)
        if ws:
            event_bus.emit('web_message_send', device_id, data)
            await ws.send_json(data)
        else:
            event_bus.emit('web_message_failed', device_id, data)


web_ws_manager = WebClientWebSocketManager()
