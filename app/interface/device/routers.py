
from fastapi import APIRouter, WebSocket

from infrastructure.devices.ws_manager import device_ws_manager
from infrastructure.devices.ws_session import device_ws_session
from infrastructure.logger_module import api_logger

logger = api_logger

router = APIRouter(prefix='/devices')


@router.websocket('/ws/{device_id}/connect')
async def device_websocket_handler(websocket: WebSocket, device_id: int):
    await websocket.accept()
    await device_ws_session.handle(websocket=websocket, device_id=device_id)


