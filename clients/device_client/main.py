import json
import asyncio
import websockets
from pyee.asyncio import AsyncIOEventEmitter
from dotenv import load_dotenv
from clients.device_client.device import DeviceImitator
import os

from clients.device_client.logger_config import get_logger

logger = get_logger("device_client")

load_dotenv()
host = os.getenv('HOST')
ws_protocol = os.getenv('WS_PROTOCOL')

event_bus = AsyncIOEventEmitter()

auth_token = 'abc123'

RECONNECT_DELAY = 3


# ------------------------------
async def websocket_client():
    while True:
        try:
            logger.info("Connecting to server...")
            async with websockets.connect(f"{ws_protocol}://{host}/devices/ws/1/connect") as websocket:
                logger.info("Websocket connected")
                await websocket.send(json.dumps({'auth_token': auth_token}))

                while True:
                    try:
                        msg = await websocket.recv()
                        if msg == 'ping':
                            await websocket.send('pong')
                            continue

                        try:
                            data = json.loads(msg)
                        except json.JSONDecodeError:
                            logger.warning(f"Bad JSON received: {msg}")
                            continue

                        event_bus.emit('message_from_server', data, websocket)

                    except websockets.ConnectionClosed as e:
                        logger.warning(f"Disconnected: {e}. Reconnecting in {RECONNECT_DELAY}s…")
                        break

                    await asyncio.sleep(0.01)

        except Exception as e:
            logger.error(f"Connection error: {e}. Reconnecting in {RECONNECT_DELAY}s…")
            await asyncio.sleep(RECONNECT_DELAY)


# ------------------------------
@event_bus.on('message_from_server')
async def handle_message(data, ws):
    logger.info(f'Message from server: {data}')
    action = data.get('action')
    pin = data.get('pin')
    pin = int(pin) if pin else None
    await device.set_ws(ws=ws)

    if action == 'set_state':
        state = data.get('state')
        await device.set_state(pin=pin, state=int(state))

    elif action == 'set_mode':
        mode = data.get('mode')
        await device.set_mode(pin=pin, mode=mode)

    elif action == 'set_schedule':
        schedule = data.get('schedule')
        on = schedule.get('on_time')
        off = schedule.get('off_time')
        await device.set_schedule(pin=pin, on_time=on, off_time=off)
    elif action == 'set_pin_name':
        await device.set_name(pin=pin, name=data.get('name'))
    elif action == 'report':
        await device.report_to()
        logger.info('Report requested')


async def run_device():
    global device
    device = DeviceImitator()
    logger.info("Device client starting")
    await asyncio.sleep(5)
    await asyncio.gather(websocket_client(), device.start())


if __name__ == "__main__":
    asyncio.run(run_device())