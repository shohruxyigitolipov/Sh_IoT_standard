from app.device.device_state import device_state
from app.events.emitters import event_bus
from app.ws.manager import ws_manager
import json

@event_bus.on('message_from_device')
async def handle_message_from_device(device_id, message):
    await ws_manager.set_response(device_id=device_id, message=message)


@event_bus.on('message_from_web')
async def handle_message_from_web(device_id, msg):

    print(f'message_from_web{device_id}: {msg}')

    try:
        data = json.loads(msg)
        msg_type = data.get("type")

        if msg_type == "set_gpio":
            pin = data["pin"]
            state = data["state"]
            await device_state.set_state(pin, state)

        elif msg_type == "set_mode":
            pin = data["pin"]
            mode = data["mode"]
            if mode == "manual":
                await device_state.set_manual(pin)
            elif mode == "auto":
                # Логика авто режима — опционально
                pass
            else:
                raise ValueError("Неверный режим")

        elif msg_type == "set_schedule":
            pin = data["pin"]
            on = data["on"]
            off = data["off"]
            await device_state.set_schedule(pin, on, off)
            await device_state.set_state(pin, 0)  # сбрасываем состояние

        elif msg_type == "ping":
            event_bus.emit('web_ping', device_id)
        else:
            pass

        # После любой команды можно отдать обновлённое состояние:
        status = {
            "pin": pin,
            "state": device_state.get_status(pin),
            "mode": device_state.get_mode(pin),
            "schedule": device_state.get_schedule(pin)
        }
        await ws_manager.send_personal(f"device{device_id}", status)

    except Exception as e:
        await ws_manager.send_personal(f"web{device_id}", {"type": "error", "message": str(e)})
