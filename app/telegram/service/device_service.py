from utils.helpers import FastConnection
from config import url


class DeviceService:
    @staticmethod
    async def get_devices():
        return await FastConnection(url=f"{url}/devices/all").request()

    @staticmethod
    async def get_active_devices():
        return await FastConnection(url=f"{url}/devices/active").request()

    @staticmethod
    async def get_device_status(device_id: int) -> bool:
        response = await FastConnection(url=f"{url}/devices/{device_id}/status").request()
        return response.get('status', False)

    @staticmethod
    async def create_device(name: str):
        return await FastConnection(url=f"{url}/devices/create").request(method='POST', data={'name': name})
