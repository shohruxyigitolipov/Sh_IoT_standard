from app.application.devices.device_service import DeviceService
from app.infrastructure.devices.in_memory_state import InMemoryDeviceStateManager
from app.infrastructure.devices.ws_sender import WebSocketDeviceSender
from app.infrastructure.web_interface.ws_sender import WebSocketWebSender


def get_device_service() -> DeviceService:
    sender = WebSocketDeviceSender()
    state_manager = InMemoryDeviceStateManager()
    sender_web = WebSocketWebSender()
    return DeviceService(sender=sender, state_manager=state_manager, sender_web=sender_web)
