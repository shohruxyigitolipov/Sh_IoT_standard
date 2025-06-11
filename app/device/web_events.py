import uuid

from app.config import event_bus
from device.managers import device_ws_manager
from device.service import DeviceCommands


# web
@event_bus.on('web_ws_connected')
async def handle_connection(websocket):
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
    # request_id = str(uuid.uuid4())
    # message['request_id'] = request_id
    await DeviceCommands(device_id=1).set_state(pin=4, state=1)
    # await device_ws_manager.send_personal(device_id=int(device_id), data=message)
