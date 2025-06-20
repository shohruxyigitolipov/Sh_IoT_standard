from app.config.config import event_bus
from app.infrastructure.logger_module.utils import get_logger_factory
from app.infrastructure.web_interface.ws_manager import web_ws_manager

get_logger = get_logger_factory('device')
logger = get_logger()


@event_bus.on("device_ws_connected")
async def handle_connect(device_id, websocket):
    logger.info(f'✅ Устройство {device_id} подключено.')


@event_bus.on("message_from_device")
async def handle_message(device_id, message):
    logger.debug(f"📨 {device_id} прислал: {message}")


@event_bus.on('message_to_device')
async def handle_message_to_device(device_id, message):
    logger.debug(f'{device_id} Отправлено сообщение: {message}')


@event_bus.on('device_send_error')
async def handle_send_error(device_id, error):
    logger.debug(f'[{device_id}], Ошибка отправки команды: {error}')


@event_bus.on('device_error')
async def handle_error(device_id, error):
    logger.debug(f"[{device_id}] Ошибка в работе устройства: {error}")


@event_bus.on('device_session_end')
async def handle_session_end(device_id):
    logger.debug(f'[{device_id}], Сессия завершена')


@event_bus.on('device_wrong_auth_token')
async def handle_auth_token_wrong(device_id):
    logger.debug(f'[{device_id}], Неверный auth_token')


@event_bus.on('message_failed')
async def handle_message_failed(device_id, message):
    logger.debug(f"[{device_id}], Сообщение: {message} возможно не дошло")
    # raise RuntimeError(f'Websocket for device {device_id} not found')
