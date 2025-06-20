from app.application.devices.device_service import DeviceService
from app.infrastructure.devices.in_memory_state import InMemoryDeviceStateManager
from app.infrastructure.devices.ws_sender import WebSocketDeviceSender
from app.infrastructure.web_interface.ws_sender import WebSocketWebSender
from app.domain.devices.interfaces import IDeviceSender, IDeviceStateManager, IWebSender


def get_device_service() -> DeviceService:
    sender: IDeviceSender = WebSocketDeviceSender()
    state_manager: IDeviceStateManager = InMemoryDeviceStateManager()
    sender_web: IWebSender = WebSocketWebSender()
    return DeviceService(sender=sender, state_manager=state_manager, sender_web=sender_web)
