import json
from fastapi import WebSocket
from app.config.config import event_bus
from app.infrastructure.devices.in_memory_state import device_state
from app.infrastructure.web_interface.ws_manager import web_ws_manager


@event_bus.on('device_ws_connected')
async def handle_connection(device_id, ws: WebSocket):
    await ws.send_json(json.dumps({"message": "Вы подключились"}))


@event_bus.on('device_ws_timeout')
async def handle_timeout(ws: WebSocket):
    await ws.send_json(json.dumps({"message": "Время ожидания истекло!"}))


@event_bus.on('device_ws_wrong_auth_token')
async def handle_device_wrong_auth_token(ws: WebSocket):
    await ws.send_json(json.dumps({'message': 'Неверный auth_token'}))  # сообщение устройству


@event_bus.on('message_from_device')
async def handle_message_from_device(device_id: int, message: str):
    message = json.loads(message)
    message_type = message.get('type')

    if message_type == 'report':
        for pin in message.get('pin_list'):
            schedule = pin.get('schedule')
            await device_state.set_state(pin=pin.get('pin'), state=pin.get('state'))
            await device_state.set_mode(pin=pin.get('pin'), mode=pin.get('mode'))
            await device_state.set_schedule(pin=pin.get('pin'), on_time=schedule.get('on_time'),
                                            off_time=schedule.get('off_time'))

        await web_ws_manager.send_personal(device_id, data=message)


@event_bus.on('device_status')
async def handle_message_failed(device_id: int, status: bool):
    await web_ws_manager.send_personal(device_id, {
        'type': 'device_status',
        'status': status
    })
