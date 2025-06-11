from app.config import event_bus
from app.logger_module.utils import get_logger_factory

get_logger = get_logger_factory(__name__)
logger = get_logger()

@event_bus.on('new_device')
async def handle_new_device(device_id):
    logger.debug(f'Новое устройство: {device_id}')

@event_bus.on("device_connected")
async def handle_connect(device_id):
    logger.debug(f'✅ Устройство {device_id} подключено.')


@event_bus.on("device_disconnected")
async def handle_disconnect(device_id):
    logger.debug(f"[{device_id}] Сессия завершена и удалена.❌")


@event_bus.on("message_from_device")
async def handle_message(device_id, message):
    logger.debug(f"📨 {device_id} прислал: {message}")


@event_bus.on('message_to_device')
async def handle_message_to_device(device_id, message):
    logger.debug(f'{device_id} Отправлено сообщение: {message}')


@event_bus.on('device_timeout')
async def handle_timeout(device_id, last_pong_time):
    logger.info(f"")


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
    raise RuntimeError(f'Websocket for device {device_id} not found')


@event_bus.on('no_reply')
async def handle_no_message(device_id, message):
    logger.debug(f"[{device_id}], Устройство не ответил на сообщение: {message}")

@event_bus.on('got_reply')
async def handle_reply_message(device_id, data, response):
    logger.debug(f'[{device_id}], Ответ от устройства. Запрос: {data}\nОтвет: {response}')
