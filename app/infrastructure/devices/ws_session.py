import asyncio

from fastapi import status
from fastapi.websockets import WebSocket, WebSocketDisconnect

from app.config.config import event_bus
from app.infrastructure.devices.ws_manager import device_ws_manager
from app.infrastructure.logger_module.utils import get_logger_factory

get_logger = get_logger_factory(__name__)
logger = get_logger()


async def verify_auth_token(token):
    auth_token = 'abc123'
    return token == auth_token


class DeviceWebSocketSession:
    async def handle(self, websocket: WebSocket, device_id: int):
        if not await self._authenticate(websocket, device_id):
            event_bus.emit('device_ws_wrong_auth_token', websocket)
            await asyncio.sleep(3)
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        event_bus.emit('device_ws_connected', device_id, websocket)
        await device_ws_manager.add(device_id, websocket)

        await self._listen(websocket, device_id)

    @staticmethod
    async def _authenticate(websocket: WebSocket, device_id: int) -> bool:
        try:
            data = await asyncio.wait_for(websocket.receive_json(), timeout=15)
        except asyncio.TimeoutError:
            event_bus.emit('device_ws_timeout', websocket)
            return False

        token = data.get("auth_token") if isinstance(data, dict) else None
        verified = await verify_auth_token(token)
        return verified

    @staticmethod
    async def _listen(websocket: WebSocket, device_id: int):
        try:
            while True:
                msg = await websocket.receive_text()
                event_bus.emit('message_from_device', device_id, msg)
        except WebSocketDisconnect:
            event_bus.emit('device_ws_disconnected', device_id)
            await device_ws_manager.remove(device_id)


device_ws_session = DeviceWebSocketSession()
