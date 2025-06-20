from app.config.config import event_bus
from app.config.container import get_device_service
from app.infrastructure.web_interface.ws_manager import web_ws_manager

device_service = get_device_service()


@event_bus.on('web_ws_disconnected')
async def handle_connection(device_id):
    await web_ws_manager.remove(device_id)


@event_bus.on('message_from_web_ws')
async def handle_message_from_device(device_id, data):
    action = data.get('action')

    if not action:
        return
    elif action == 'set_state':
        await device_service.set_state(device_id, pin=data['pin'], state=data['state'])
    elif action == 'set_mode':
        await device_service.set_mode(device_id, pin=data.get('pin'), mode=data.get('mode'))
    elif action == 'get_report':
        await device_service.request_report(device_id, pin=data.get('pin'))
    elif action == 'set_schedule':
        schedule = data.get('schedule')
        await device_service.set_schedule(
            device_id,
            pin=data.get('pin'),
            on_time=schedule.get('on_time'),
            off_time=schedule.get('off_time')
        )
