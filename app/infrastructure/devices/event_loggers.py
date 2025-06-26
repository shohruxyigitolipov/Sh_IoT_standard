from app.config import event_bus
from app.infrastructure.logger_module.utils import get_logger_factory

get_logger = get_logger_factory('device')
logger = get_logger()


@event_bus.on("device_ws_connected")
async def handle_connect(device_id, websocket):
    logger.critical(f'✅ Device {device_id} connected.')


@event_bus.on("message_from_device")
async def handle_message(device_id, message):
    logger.debug(f"📨 {device_id} sent: {message}")


@event_bus.on('message_to_device')
async def handle_message_to_device(device_id, message):
    logger.debug(f'Message sent to {device_id}: {message}')


@event_bus.on('device_send_error')
async def handle_send_error(device_id, error):
    logger.debug(f'[{device_id}] Command sending error: {error}')


@event_bus.on('device_error')
async def handle_error(device_id, error):
    logger.debug(f"[{device_id}] Device error: {error}")


@event_bus.on('device_session_end')
async def handle_session_end(device_id):
    logger.debug(f'[{device_id}] Session closed')


@event_bus.on('device_wrong_auth_token')
async def handle_auth_token_wrong(device_id):
    logger.debug(f'[{device_id}] Invalid auth_token')


@event_bus.on('device_message_failed')
async def handle_message_failed(device_id, message):
    logger.debug(f"[{device_id}] Message may not have been delivered: {message}")
