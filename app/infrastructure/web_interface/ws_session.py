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
    async def handle(self, ws: WebSocket, device_id: int):
        if not await self._authenticate(ws):
            event_bus.emit('web_ws_wrong_auth_token', ws)
            await asyncio.sleep(3)
            await ws.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        await web_ws_manager.add(device_id=device_id, ws=ws)
        await self._listen(ws, device_id)

    @staticmethod
    async def _authenticate(ws: WebSocket) -> bool:
        try:
            data = await asyncio.wait_for(ws.receive_json(), timeout=15)
        except asyncio.TimeoutError:
            event_bus.emit('web_ws_timeout', ws)
            return False
        token = data.get('auth_token', None)
        verified = await verify_auth_token(token)
        return verified

    @staticmethod
    async def _listen(ws: WebSocket, device_id: int):
        try:
            while True:
                data = await ws.receive_json()
                event_bus.emit('message_from_web_ws', device_id, data)
        except WebSocketDisconnect:
            web_ws_manager.remove(device_id)
        except Exception as e:
            logger.exception(f'[{device_id}] Error in web ws session: {e}')
            web_ws_manager.remove(device_id)


web_ws_session = WebClientWebSocketSession()
