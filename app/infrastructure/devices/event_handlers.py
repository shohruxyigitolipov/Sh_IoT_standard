import json
from fastapi import WebSocket
from app.config import event_bus
from app.infrastructure.devices.redis_state import device_state
from app.infrastructure.web_interface.ws_manager import web_ws_manager


@event_bus.on('device_ws_connected')
async def handle_connection(device_id, ws: WebSocket):
    await ws.send_json({'message': 'Вы подключились'})
    await ws.send_json(await device_state.get_init_state(device_id))
    event_bus.emit('device_status', device_id, True)


@event_bus.on('device_ws_disconnected')
async def handle_disconnection(device_id):
    event_bus.emit('device_status', device_id, False)


@event_bus.on('device_ws_timeout')
async def handle_timeout(ws: WebSocket):
    await ws.send_json({'message': 'Время ожидания истекло!'})


@event_bus.on('device_ws_wrong_auth_token')
async def handle_device_wrong_auth_token(ws: WebSocket):
    await ws.send_json({'message': 'Неверный auth_token'})


@event_bus.on('message_from_device')
async def handle_message_from_device(device_id: int, message: str):
    message = json.loads(message)
    message_type = message.get('type')

    if message_type == 'report':
        for pin in message.get('pin_list'):
            schedule = pin.get('schedule')
            await device_state.set_state(device_id, pin=pin.get('pin'), state=pin.get('state'))
            await device_state.set_mode(device_id, pin=pin.get('pin'), mode=pin.get('mode'))
            await device_state.set_schedule(
                device_id,
                pin=pin.get('pin'),
                on_time=schedule.get('on_time'),
                off_time=schedule.get('off_time')
            )
            await device_state.set_name(device_id, pin=pin.get('pin'), name=pin.get('name', None))

        report = await device_state.save_report(device_id)
        await web_ws_manager.send_personal(device_id, data=report)


@event_bus.on('device_status')
async def handle_message_failed(device_id: int, status: bool):
    await web_ws_manager.send_personal(device_id, {
        'type': 'device_status',
        'status': status
    })
