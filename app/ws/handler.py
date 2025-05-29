from app.events.emitters import event_bus
from fastapi.websockets import WebSocket, WebSocketDisconnect
import asyncio
from fastapi import status
from app.ws.manager import ws_manager


async def verify_auth_token(token):
    auth_token = 'abc123'
    return token == auth_token


class WsHandler:
    async def handle_connection(self, websocket: WebSocket, device_id: int):
        if not await self._authenticate(websocket, device_id):
            event_bus.emit('device_wrong_auth_token', device_id, websocket)
            await asyncio.sleep(3)
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        event_bus.emit('device_connected', device_id)
        await ws_manager.add(device_id, websocket)
        await self._listen(websocket, device_id)

    @staticmethod
    async def _authenticate(websocket: WebSocket, device_id: int) -> bool:
        try:
            data = await asyncio.wait_for(websocket.receive_json(), timeout=15)
        except asyncio.TimeoutError:
            event_bus.emit('device_timeout', device_id)
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
                    event_bus.emit('device_ping', device_id)
                else:
                    event_bus.emit('message_from_device', device_id, msg)
        except WebSocketDisconnect:
            event_bus.emit('websocket_disconnected', device_id)
            await ws_manager.remove(device_id)


ws_handler = WsHandler()


@event_bus.on('device_connected')
async def handle_connection(device_id):
    await ws_manager.send_personal(device_id, 'Вы подключились')


@event_bus.on('device_timeout')
async def handle_timeout(device_id):
    await ws_manager.send_personal(device_id, 'Время ожидания истекло!')


@event_bus.on('device_wrong_auth_token')
async def handle_wrong_auth_token(device_id, websocket):
    await websocket.send_text('Неверный auth_token')  # сообщение устройству


@event_bus.on('message_from_device')
async def handle_message_from_device(device_id, message):
    await ws_manager.set_response(device_id=device_id, message=message)
