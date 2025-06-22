import json
import asyncio
import websockets
from pyee.asyncio import AsyncIOEventEmitter
from dotenv import load_dotenv
from device_client.device import DeviceImitator
import os

device = DeviceImitator()
load_dotenv('.env')
host = os.getenv('HOST')

event_bus = AsyncIOEventEmitter()

auth_token = 'abc123'

RECONNECT_DELAY = 3

global ws_connection


# ------------------------------
async def websocket_client():
    global ws_connection
    while True:
        try:
            async with websockets.connect(f"ws://{host}/devices/ws/1/connect") as websocket:
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
                            print(f"[{now()}] ⚠️ Bad JSON:", msg)
                            continue

                        event_bus.emit('message_from_server', data, websocket)

                    except websockets.ConnectionClosed as e:
                        print(f"[{now()}] 🔌 Disconnected: {e}. Reconnecting in {RECONNECT_DELAY}s…")
                        break

                    await asyncio.sleep(0.01)

        except Exception as e:
            print(f"[{now()}] ❌ Connection error: {e}. Reconnecting in {RECONNECT_DELAY}s…")
            await asyncio.sleep(RECONNECT_DELAY)


# ------------------------------
@event_bus.on('message_from_server')
async def handle_message(msg, ws):
    try:
        data = json.loads(msg)
    except:
        print(f"Not JSON: {msg}")
        return
    print(f'Message from server: {data}')
    action = data.get('action')
    pin = data.get('pin')
    pin = int(pin) if pin else None
    await device.set_ws(websocket=ws)

    if action == 'set_state':
        state = data.get('state')
        await device.set_state(pin=pin, state=int(state))
        print(f"[{now()}] ⚙️ GPIO {pin} set to {state}")

    elif action == 'set_mode':
        mode = data.get('mode')
        await device.set_mode(pin=pin, mode=mode)
        print(f"[{now()}] 🔁 Mode set for GPIO {pin}: {mode}")

    elif action == 'set_schedule':
        schedule = data.get('schedule')
        on = schedule.get('on_time')
        off = schedule.get('off_time')
        await device.set_schedule(pin=pin, on_time=on, off_time=off)
        print(f"[{now()}] ⏱ Schedule set for GPIO {pin}: on - {on}, off - {off}")
    elif action == 'set_pin_name':
        await device.set_name(pin=pin, name=data.get('name'))
        print(f"[{now()}] 🏷 Name set for GPIO {pin}: {data.get('name')}")
    elif action == 'report':
        await device.report_to()


# ------------------------------
def now():
    return f"{asyncio.get_event_loop().time():.1f}"


async def run_device():
    await asyncio.sleep(5)
    await asyncio.gather(websocket_client(), device.start())
