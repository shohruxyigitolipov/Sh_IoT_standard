import json
from fastapi import WebSocket
from app.config import event_bus
from app.infrastructure.logger_module.utils import get_logger_factory

get_logger = get_logger_factory('Web Interface')
logger = get_logger()


# web
@event_bus.on('web_ws_connected')
async def handle_connection(device_id, ws: WebSocket):
    logger.info(f'{[device_id]} Веб-интерфейс подключен')
    await ws.send_json(json.dumps({'message': 'Вы подключились'}))


@event_bus.on('web_ws_disconnected')
async def handle_disconnection(device_id):
    logger.info(f'{[device_id]} Веб-интерфейс отключен')


@event_bus.on('web_ws_timeout')
async def handle_timeout(ws: WebSocket):
    await ws.send_json(json.dumps({'message': 'Время ожидания истекло!'}))


@event_bus.on('web_ws_wrong_auth_token')
async def handle_web_wrong_auth_token(ws: WebSocket):
    await ws.send_json(json.dumps({'message': 'Неверный auth_token'}))  # сообщение устройству


@event_bus.on('web_ws_timeout')
async def handle_timeout(ws: WebSocket):
    pass


@event_bus.on('web_ws_wrong_auth_token')
async def handle_web_wrong_auth_token(ws: WebSocket):
    pass


@event_bus.on('message_from_web_ws')
async def handle_message_from_device(device_id, message):
    print(f'[{device_id}] message from web: {message}')
