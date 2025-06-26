import json
from fastapi import WebSocket
from app.config import event_bus
from app.infrastructure.logger_module.utils import get_logger_factory

get_logger = get_logger_factory('Web Interface')
logger = get_logger()


# web
@event_bus.on('web_ws_connected')
async def handle_connection(device_id, ws: WebSocket):
    logger.info(f'{[device_id]} Web interface connected')


@event_bus.on('web_ws_disconnected')
async def handle_disconnection(device_id):
    logger.info(f'{[device_id]} Web interface disconnected')


@event_bus.on('web_ws_timeout')
async def handle_timeout(ws: WebSocket):
    logger.warning('Web interface timeout')


@event_bus.on('web_ws_wrong_auth_token')
async def handle_web_wrong_auth_token(ws: WebSocket):
    logger.warning('Web interface wrong auth token')


@event_bus.on('message_from_web_ws')
async def handle_message_from_device(device_id, message):
    logger.info(f'[{device_id}] Message from web: {message}')


@event_bus.on('web_message_send')
async def handle_web_message_send(device_id, message):
    logger.info(f'[{device_id}] Send to web: {message}')


@event_bus.on('web_message_failed')
async def handle_web_message_failed(device_id, message):
    logger.warning(f'[{device_id}] Failed to send to web: {message}')