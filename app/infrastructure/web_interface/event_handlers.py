from app.config.config import const_pins
from app.config.config import event_bus
from app.config.container import get_device_service
from app.infrastructure.web_interface.ws_manager import web_ws_manager

device_service = get_device_service()


@event_bus.on('message_from_web_ws')
async def handle_message_from_device(device_id, message):
    action = message.get('action')
    print(message)
    if not action:
        return
    if action == 'set_state':
        await device_service.set_state(device_id, pin=message['pin'], state=message['state'])
    if action == 'set_mode':
        await device_service.set_mode(device_id, pin=message.get('pin'), mode=message.get('mode'))
    if action == 'get_report':
        await device_service.request_report(device_id, pin=message.get('pin'))
