from starlette.websockets import WebSocket

from app.config import event_bus
from app.infrastructure.devices.redis_state import device_state
from app.infrastructure.devices.ws_manager import device_ws_manager
from app.infrastructure.web_interface.ws_manager import web_ws_manager


@event_bus.on('web_ws_connected')
async def handle_connection(device_id, ws: WebSocket):
    status = device_id in device_ws_manager.active
    event_bus.emit('device_status', device_id, status)


@event_bus.on('web_ws_disconnected')
async def handle_disconnection(device_id):
    await web_ws_manager.remove(device_id)


@event_bus.on('message_from_web_ws')
async def handle_message_from_device(device_id, data):
    action = data.get('action')
    
    match action:
        case 'get_report':
            await web_ws_manager.send_personal(device_id, data=await device_state.get_report(device_id))
        case 'set_pin_name', pin, name:
            await device_state.set_name(device_id, pin, name)
            await device_state.save_report(device_id)
        case None:
            pass
        case _:
            await device_ws_manager.send_personal(device_id, data=data)
