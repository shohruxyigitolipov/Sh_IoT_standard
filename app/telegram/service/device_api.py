from utils.helpers import FastConnection
from config import url


class DeviceAPI:
    @staticmethod
    async def send_state(device_id: int, state: int):
        conn = FastConnection(url=f"{url}/devices/control/{device_id}")
        return await conn.request(method='POST', data={'state': state})

    @staticmethod
    async def clear_timer(device_id: int):
        conn = FastConnection(url=f"{url}/devices/control/{device_id}")
        return await conn.request(method='POST')

    @staticmethod
    async def set_timer(device_id: int, start: str, stop: str):
        data = {
            "start_time": start,
            "stop_time": stop
        }
        conn = FastConnection(url=f"{url}/devices/control/{device_id}")
        return await conn.request(method='POST', data=data)

    @staticmethod
    async def get_status(device_id: int):
        conn = FastConnection(url=f"{url}/devices/{device_id}/status")
        return await conn.request()

    @staticmethod
    async def active_devices():
        conn = FastConnection(url=f"{url}/devices/active")
        return await conn.request()

    @staticmethod
    async def devices_all():
        conn = FastConnection(url=f"{url}/devices/all")
        return await conn.request()

    @staticmethod
    async def device_create(device_name: str):
        conn = FastConnection(url=f"{url}/devices/create")
        return await conn.request(method='POST', data={'name': device_name})
