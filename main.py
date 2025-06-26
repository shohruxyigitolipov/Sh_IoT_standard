import asyncio
import uvicorn
from app.config import DEVICE_RUN
from clients.device_client.main import run_device
from clients.telegram_client.bot import run_telegram_bot

async def start_server():
    await asyncio.to_thread(
        uvicorn.run,
        "app.main:app",
        host="0.0.0.0",
        port=8000,
    )

async def main():
    tasks = [
        asyncio.create_task(start_server()),
        asyncio.create_task(run_telegram_bot()),
    ]
    if DEVICE_RUN:
        tasks.append(asyncio.create_task(run_device()))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
