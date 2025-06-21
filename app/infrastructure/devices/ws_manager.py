import json

from fastapi import WebSocket

from app.config import event_bus
from app.infrastructure.logger_module.utils import get_logger_factory

get_logger = get_logger_factory(__name__)
logger = get_logger()


class DeviceWebSocketManager:
    def __init__(self):
        self.active: dict[int, WebSocket] = {}

    async def add(self, device_id: int, ws: WebSocket):
        self.active[device_id] = ws
        event_bus.emit('device_status', device_id, True)

    async def remove(self, device_id: int):
        try:
            await self.active.pop(device_id, None).close()
        except Exception as e:
            pass
        event_bus.emit('device_status', device_id, False)

    async def send_personal(self, device_id: int, data: str | dict) -> dict | None | bool:
        ws = self.active.get(device_id)
        if ws:
            if isinstance(data, dict):
                data = json.dumps(data)
            await ws.send_json(data)
        else:
            event_bus.emit('message_failed', device_id, data)


device_ws_manager = DeviceWebSocketManager()
