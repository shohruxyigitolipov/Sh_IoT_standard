from app.config.config import event_bus
from app.config.container import get_device_service

device_service = get_device_service()


# web
@event_bus.on('web_ws_connected')
async def handle_connection(device_id, websocket):
    await websocket.send_text('Вы подключились')


@event_bus.on('web_ws_timeout')
async def handle_timeout(websocket):
    await websocket.send_text('Время ожидания истекло!')


@event_bus.on('web_ws_wrong_auth_token')
async def handle_web_wrong_auth_token(websocket):
    await websocket.send_text('Неверный auth_token')  # сообщение устройству


@event_bus.on('message_from_web_ws')
async def handle_message_from_device(device_id, message):
    print(f'[{device_id}] message from web: {message}')
    await device_service.set_state(device_id=device_id, pin=4, state=1)

