from fastapi import APIRouter, WebSocket

from app.infrastructure.logger_module.utils import get_logger_factory
from app.infrastructure.web_interface.ws_session import web_ws_session

get_logger = get_logger_factory(__name__)
logger = get_logger()

router = APIRouter(prefix='/interfaces/web')


@router.websocket('/ws/{device_id}/connect')
async def web_websocket_handler(ws: WebSocket, device_id: int):
    await ws.accept()
    await web_ws_session.handle(ws=ws, device_id=device_id)
