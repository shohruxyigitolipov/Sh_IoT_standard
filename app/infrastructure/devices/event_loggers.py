from app.config import event_bus
from app.infrastructure.logger_module.utils import get_logger_factory

get_logger = get_logger_factory('device')
logger = get_logger()


@event_bus.on("device_ws_connected")
async def handle_connect(device_id, websocket):
    logger.info(f'[{device_id}] Device connected')


event_bus.on("device_ws_disconnected")
async def handle_disconnect(device_id):
    logger.info(f'[{device_id}] Device disconnected')


@event_bus.on("message_from_device")
async def handle_message(device_id, message):
    logger.debug(f"[{device_id}] Device sent: {message}")


@event_bus.on('device_error')
async def handle_error(device_id, error):
    logger.debug(f"[{device_id}] Device error: {error}")


@event_bus.on('device_session_end')
async def handle_session_end(device_id):
    logger.debug(f'[{device_id}] Devices session closed')


@event_bus.on('device_wrong_auth_token')
async def handle_auth_token_wrong(device_id):
    logger.debug(f'[{device_id}] Invalid auth_token')


@event_bus.on('device_message_send')
async def handle_message_send(device_id, data):
    logger.debug(f'[{device_id}] Send to device: {data}')


@event_bus.on('device_message_failed')
async def handle_message_failed(device_id, message):
    logger.warning(f'[{device_id}] Failed to send to device: {message}')
