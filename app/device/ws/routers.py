from fastapi import APIRouter
from fastapi import WebSocket

from device.ws import ws_handler, web_ws_handler
from infrastructure.logger_module import api_logger

logger = api_logger

router = APIRouter(prefix='/devices')


@router.websocket('/ws/{device_id}/connect')
async def device_websocket_handler(websocket: WebSocket, device_id: int):
    await websocket.accept()
    await ws_handler.handle(websocket=websocket, device_id=device_id)


@router.websocket('/ws/web/{device_id}/connect')
async def web_websocket_handler(websocket: WebSocket, device_id: int):
    await websocket.accept()
    await web_ws_handler.handle(websocket=websocket, device_id=device_id)
