import json

from app.config.config import event_bus
from app.infrastructure.devices.ws_manager import device_ws_manager
from app.infrastructure.web_interface.ws_manager import web_ws_manager


@event_bus.on('device_ws_connected')
async def handle_connection(device_id, websocket):
    await websocket.send_text('Вы подключились')


@event_bus.on('device_ws_timeout')
async def handle_timeout(device_id):
    await device_ws_manager.send_personal(device_id, 'Время ожидания истекло!')


@event_bus.on('device_ws_wrong_auth_token')
async def handle_device_wrong_auth_token(websocket):
    await websocket.send_text('Неверный auth_token')  # сообщение устройству


@event_bus.on('message_from_device_ws')
async def handle_message_from_device(device_id, message):
    print(f'[{device_id}] device_msg: {message}')
    # await device_ws_manager.set_response(device_id=device_id, response=message)
    message = json.loads(message)
    message_type = message.get('type')
    print(message)
    if message_type == 'report':
        await web_ws_manager.send_personal(device_id, message)

@event_bus.on('device_status')
async def handle_message_failed(device_id, status: bool):
    await web_ws_manager.send_personal(device_id, {
        'type': 'device_status',
        'status': status
    })