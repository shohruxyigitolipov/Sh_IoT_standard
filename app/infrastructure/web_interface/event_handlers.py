import json

from app.config.config import event_bus
from app.config.container import get_device_service
from config.config import const_pins
from infrastructure.web_interface.ws_manager import web_ws_manager

device_service = get_device_service()


@event_bus.on('message_from_web_ws')
async def handle_message_from_device(device_id, message):
    # message = json.loads
    action = message.get('action')
    if not action:
        return

    if action == 'set_state':
        await device_service.set_state(device_id, pin=message['pin'], state=message['state'])
    if action == 'get_pins':
        payload = {'type': 'pin_list', 'list': []}
        for pin in const_pins:
            state = await device_service.get_state(pin=pin)
            mode = await device_service.get_mode(pin=pin)
            payload['list'].append({'pin': pin, 'state': state, 'mode': mode})
        print(payload)
        await web_ws_manager.send_personal(device_id=device_id, data=payload)
