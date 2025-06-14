import uuid

from device.ws.websocket_connection_manager import device_ws_manager, web_ws_manager
from domain.devices.interfaces import IDeviceSender, IWebSender


class WebSocketDeviceSender(IDeviceSender):
    async def send(self, device_id: int, data: dict) -> dict:
        request_id = str(uuid.uuid4())
        return await device_ws_manager.send_personal(device_id=device_id, data=data, timeout=15, request_id=request_id)


class WebSocketWebSender(IWebSender):
    async def send(self, device_id: int, data: dict) -> dict:
        return await web_ws_manager.send_personal(device_id=device_id, data=data)
