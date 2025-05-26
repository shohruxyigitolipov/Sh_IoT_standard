import asyncio
import json
from typing import Dict
from app.events.emitters import event_bus
from fastapi import WebSocket


class WSConnectionManager:
    def __init__(self):
        self.active: dict[str, WebSocket] = {}
        self.pending = {}

    async def add(self, device_id: str, ws: WebSocket):
        self.active[device_id] = ws
        event_bus.emit('websocket_added', device_id)

    async def remove(self, device_id: str) -> bool:
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

    async def broadcast(self, message: dict | str):
        payload = json.dumps(message, ensure_ascii=False)
        tasks = [
            self._safe_send(device_id, ws, payload)
            for device_id, ws in list(self.active.items())
        ]
        await asyncio.gather(*tasks)

    @staticmethod
    async def _safe_send(device_id, ws, payload):
        try:
            await ws.send_text(payload)
        except:
            event_bus.emit('message_failed', device_id, payload)

    async def send_personal(self, device_id: str, data: str | dict,
                            request_id: str = None, timeout: float = 5) -> dict | None | bool:
        ws = self.active.get(device_id)
        if not ws:
            event_bus.emit('message_failed', device_id, data)
            return False
        if isinstance(data, str):
            payload = data
        elif isinstance(data, dict):
            if request_id:
                data["request_id"] = request_id
            payload = json.dumps(data, ensure_ascii=False)
        else:
            raise TypeError("message должен быть str или dict")

        await ws.send_text(payload)
        if request_id:
            future = asyncio.get_event_loop().create_future()
            self.pending.setdefault(device_id, {})[request_id] = future
            try:
                response = await asyncio.wait_for(future, timeout=timeout)
                event_bus.emit('got_reply', device_id, data, str(response))
                return response
            except asyncio.TimeoutError:
                event_bus.emit(f'no_reply', device_id, data)
            finally:
                self.pending[device_id].pop(request_id, None)

        return None

    async def set_response(self, device_id: str, message: dict | str):
        if isinstance(message, str):
            try:
                message = json.loads(message)
            except Exception as e:
                logger.error(f"Ошибка при разборе сообщения от {device_id}: {e}\n{message}")
                return

        request_id = message.get('request_id', None)
        if request_id and device_id in self.pending and request_id in self.pending[device_id]:
            future = self.pending[device_id][request_id]
            if not future.done():
                future.set_result(message)
        return


ws_manager = WSConnectionManager()


@event_bus.on('websocket_added')
async def handle_new_ws(device_id):
    pass


@event_bus.on('message_failed')
async def handle_message_failed(device_id, message):
    pass


@event_bus.on('no_reply')
async def handle_no_reply(device_id, data):
    pass


@event_bus.on('got_reply')
async def handle_got_reply(device_id, data, response):
    pass
