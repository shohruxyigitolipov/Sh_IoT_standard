from config.config import event_bus
from fastapi import WebSocket
import json
import asyncio
from infrastructure.logger_module import api_logger

logger = api_logger


class WebClientWebSocketManager:
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


web_ws_manager = WebClientWebSocketManager()
