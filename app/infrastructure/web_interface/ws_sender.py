from domain.devices.interfaces import IWebSender
from infrastructure.web_interface.ws_manager import web_ws_manager


class WebSocketWebSender(IWebSender):
    async def send(self, device_id: int, data: dict) -> dict:
        return await web_ws_manager.send_personal(device_id=device_id, data=data)
