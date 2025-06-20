import json

from fastapi import WebSocket

from app.config.config import event_bus
from app.infrastructure.logger_module.utils import get_logger_factory

get_logger = get_logger_factory(__name__)
logger = get_logger()


class DeviceWebSocketManager:
    def __init__(self):
        self.active: dict[int, WebSocket] = {}

    async def add(self, device_id: int, ws: WebSocket):
        self.active[device_id] = ws
        event_bus.emit('device_status', device_id, True)

    async def remove(self, device_id: int) -> bool:
        event_bus.emit('device_status', device_id, False)
        try:
            self.active.pop(device_id, None)
        except Exception as e:
            logger.error(e)
            return False
        return True

    async def send_personal(self, device_id: int, data: str | dict) -> dict | None | bool:
        try:
            ws = self.active[device_id]
            if isinstance(data, dict):
                data = json.dumps(data, ensure_ascii=False)
            await ws.send_json(data)
        except Exception as e:
            event_bus.emit('message_failed', device_id, data)
            logger.error(e)


device_ws_manager = DeviceWebSocketManager()
