import uuid

from domain.devices.interfaces import IDeviceSender, IWebSender
from infrastructure.devices.ws_manager import device_ws_manager


class WebSocketDeviceSender(IDeviceSender):
    async def send(self, device_id: int, data: dict) -> dict:
        request_id = str(uuid.uuid4())
        return await device_ws_manager.send_personal(device_id=device_id, data=data, timeout=15, request_id=request_id)



