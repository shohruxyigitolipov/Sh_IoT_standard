import aiohttp
import asyncio
import json


class FastConnection:
    def __init__(self, url: str):
        self.url = url

    async def request(self, method: str = "GET", data: dict = None, headers: dict = None):
        async with aiohttp.ClientSession() as session:
            async with session.request(method, self.url, json=data, headers=headers) as response:
                response.raise_for_status()  # выбросит ошибку, если код не 2xx
                try:
                    return await response.json()
                except aiohttp.ContentTypeError:
                    return await response.text()
