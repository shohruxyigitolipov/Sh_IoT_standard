from fastapi import APIRouter, WebSocket
from app.infrastructure.devices.ws_session import device_ws_session
from app.infrastructure.logger_module.utils import get_logger_factory

get_logger = get_logger_factory(__name__)
logger = get_logger()

router = APIRouter(prefix='/devices')


@router.websocket('/ws/{device_id}/connect')
async def device_websocket_handler(websocket: WebSocket, device_id: int):
    await websocket.accept()
    await device_ws_session.handle(websocket=websocket, device_id=device_id)
