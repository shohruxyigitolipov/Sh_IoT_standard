import asyncio

from fastapi import status
from fastapi.websockets import WebSocket, WebSocketDisconnect

from app.config import event_bus
from app.infrastructure.web_interface.ws_manager import web_ws_manager
from app.infrastructure.logger_module.utils import get_logger_factory

get_logger = get_logger_factory(__name__)
logger = get_logger()


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
        logger.info('web_ws_connected')
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
                data = await websocket.receive_json()
                event_bus.emit('message_from_web_ws', device_id, data)
        except WebSocketDisconnect:
            event_bus.emit('web_ws_disconnected', device_id)
        except Exception as e:
            logger.exception(f'Error in web ws session {device_id}: {e}')
            event_bus.emit('web_ws_disconnected', device_id)


web_ws_session = WebClientWebSocketSession()
