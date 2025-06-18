import asyncio

from fastapi import status
from fastapi.websockets import WebSocket, WebSocketDisconnect

from app.config.config import event_bus
from infrastructure.web_interface.ws_manager import web_ws_manager


async def verify_auth_token(token):
    auth_token = 'abc123'
    return token == auth_token


class WebClientWebSocketSession:
    async def handle(self, websocket: WebSocket, device_id: int):
        if not await self._authenticate(websocket):
            event_bus.emit('web_ws_wrong_auth_token', websocket)
            await asyncio.sleep(3)
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        event_bus.emit('web_ws_connected', device_id, websocket)
        await web_ws_manager.add(device_id=device_id, ws=websocket)
        await self._listen(websocket, device_id)

    @staticmethod
    async def _authenticate(websocket: WebSocket) -> bool:
        try:
            data = await asyncio.wait_for(websocket.receive_json(), timeout=15)
        except asyncio.TimeoutError:
            event_bus.emit('web_ws_timeout', websocket)
            return False
        token = data.get('auth_token', None)
        verified = await verify_auth_token(token)
        return verified

    @staticmethod
    async def _listen(websocket: WebSocket, device_id: int):
        try:
            while True:
                msg = await websocket.receive_json()
                event_bus.emit('message_from_web_ws', device_id, msg)
        except WebSocketDisconnect:
            event_bus.emit('web_ws_disconnected')

            raise


web_ws_session = WebClientWebSocketSession()
