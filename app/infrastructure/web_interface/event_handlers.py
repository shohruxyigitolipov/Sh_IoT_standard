from app.application.devices.commands import SetState, SetMode, SetSchedule
from app.config.config import event_bus
from app.config.container import get_device_service
from app.infrastructure.devices.in_memory_state import device_state
from app.infrastructure.devices.ws_manager import device_ws_manager
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
    if action == 'get_report':
        await web_ws_manager.send_personal(device_id, data=await device_state.get_report())
    else:
        await device_ws_manager.send_personal(device_id, data=data)
