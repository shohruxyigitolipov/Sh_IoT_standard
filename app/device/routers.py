from fastapi import WebSocket

from device.service import DeviceCommands
from app.device.ws_handler import ws_handler
from app.device.ws_manager import device_ws_manager, web_ws_manager

from app.logger_module.utils import get_logger_factory
from fastapi import APIRouter

from device.ws_handler import web_ws_handler

get_logger = get_logger_factory(__name__)
logger = get_logger()

router = APIRouter(prefix='/devices')


@router.websocket('/ws/{device_id}/connect')
async def device_websocket_handler(websocket: WebSocket, device_id: int):
    await websocket.accept()
    await ws_handler.handle(websocket=websocket, device_id=device_id)


@router.websocket('/ws/web/{device_id}/connect')
async def web_websocket_handler(websocket: WebSocket, device_id: int):
    await websocket.accept()
    await web_ws_handler.handle(websocket=websocket, device_id=device_id)
