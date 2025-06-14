from fastapi import APIRouter, WebSocket

from infrastructure.logger_module import api_logger
from infrastructure.web_interface.ws_session import web_ws_session

logger = api_logger

router = APIRouter(prefix='/interfaces/web')


@router.websocket('/ws/{device_id}/connect')
async def web_websocket_handler(websocket: WebSocket, device_id: int):
    await websocket.accept()
    await web_ws_session.handle(websocket=websocket, device_id=device_id)
