from app.config import event_bus
from fastapi.websockets import WebSocket, WebSocketDisconnect
import asyncio
from fastapi import status

from app.device.ws_manager import web_ws_manager, device_ws_manager
from app.logger_module.utils import get_logger_factory

get_logger = get_logger_factory(__name__)
logger = get_logger()


async def verify_auth_token(token):
    auth_token = 'abc123'
    return token == auth_token


class WebWsHandler:
    async def handle(self, websocket: WebSocket, device_id: int):
        if not await self._authenticate(websocket, device_id):
            event_bus.emit('web_ws_wrong_auth_token', device_id, websocket)
            await asyncio.sleep(3)
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        event_bus.emit('web_ws_connected', device_id)
        await web_ws_manager.add(device_id=device_id, ws=websocket)
        await self._listen(websocket, device_id)

    @staticmethod
    async def _authenticate(websocket: WebSocket, device_id: int) -> bool:
        try:
            data = await asyncio.wait_for(websocket.receive_json(), timeout=15)
        except asyncio.TimeoutError:
            event_bus.emit('web_ws_timeout', device_id)
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


class DeviceWsHandler:
    async def handle(self, websocket: WebSocket, device_id: int):
        if not await self._authenticate(websocket, device_id):
            event_bus.emit('device_ws_wrong_auth_token', device_id, websocket)
            await asyncio.sleep(3)
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        event_bus.emit('device_ws_connected', device_id)
        await device_ws_manager.add(device_id, websocket)
        await self._listen(websocket, device_id)

    @staticmethod
    async def _authenticate(websocket: WebSocket, device_id: int) -> bool:
        try:
            data = await asyncio.wait_for(websocket.receive_json(), timeout=15)
        except asyncio.TimeoutError:
            event_bus.emit('device_ws_timeout', device_id)
            return False

        token = data.get("auth_token") if isinstance(data, dict) else None
        verified = await verify_auth_token(token)
        return verified

    @staticmethod
    async def _listen(websocket: WebSocket, device_id: int):
        try:
            while True:
                msg = await websocket.receive_text()
                if 'ping' in msg:
                    event_bus.emit('device_ws_ping', device_id)
                else:
                    event_bus.emit('message_from_device_ws', device_id, msg)
        except WebSocketDisconnect:
            event_bus.emit('device_ws_disconnected', device_id)
            await device_ws_manager.remove(device_id)


ws_handler = DeviceWsHandler()
web_ws_handler = WebWsHandler()


@event_bus.on('device_ws_connected')
async def handle_connection(device_id):
    await device_ws_manager.send_personal(device_id, 'Вы подключились')


@event_bus.on('device_ws_timeout')
async def handle_timeout(device_id):
    await device_ws_manager.send_personal(device_id, 'Время ожидания истекло!')


@event_bus.on('device_ws_wrong_auth_token')
async def handle_wrong_auth_token(device_id, websocket):
    await websocket.send_text('Неверный auth_token')  # сообщение устройству


@event_bus.on('message_from_device_ws')
async def handle_message_from_device(device_id, message):
    print(f'[{device_id}] device_msg: {message}')


# web
@event_bus.on('web_ws_connected')
async def handle_connection(device_id):
    await device_ws_manager.send_personal(device_id, 'Вы подключились')


@event_bus.on('web_ws_timeout')
async def handle_timeout(device_id):
    await device_ws_manager.send_personal(device_id, 'Время ожидания истекло!')


@event_bus.on('web_ws_wrong_auth_token')
async def handle_wrong_auth_token(websocket):
    await websocket.send_text('Неверный auth_token')  # сообщение устройству


@event_bus.on('message_from_web_ws')
async def handle_message_from_device(device_id, message):
    print(f'[{device_id}] message from web: {message}')
