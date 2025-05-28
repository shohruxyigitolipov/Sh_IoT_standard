from fastapi import APIRouter, WebSocket, Depends

from app.device.adapters import DeviceCommands

from app.device.device_state import device_state
from app.device.schemas import *
from app.events.emitters import event_bus
from app.logger_module.utils import get_logger_factory
from app.ws.handler import ws_handler as websocket_handler
from app.ws.manager import ws_manager
from fastapi import APIRouter, HTTPException
from app.device.schemas import PinAction, ScheduleData, ModeData

get_logger = get_logger_factory(__name__)
logger = get_logger()

router = APIRouter(prefix='/devices')


@router.websocket('/ws/{device_id}/connect')
async def websocket_connection(websocket: WebSocket, device_id: int):
    await websocket.accept()
    logger.info('⏳Установлена временная связь.\n'
                ' Ожидание дополнительных данных...')
    await websocket_handler.handle_connection(websocket=websocket, device_id=device_id)


@router.get('/{device_id}/status', response_model=DeviceStatus_response)
async def get_device_status_r(device_id: int):
    devices = await ws_manager.get_list()
    return DeviceStatus_response(device_id=device_id, status=device_id in devices)


device = DeviceCommands(device_id=1)  # временно фиксирован


@router.post("/1/gpio")
async def gpio_action(data: PinAction):
    if device_state.get_mode(data.pin) != "manual":
        raise HTTPException(status_code=400, detail="Пин в режиме АВТО")
    try:
        await device.set_state(data.pin, data.state)
    except:
        event_bus.emit('set_state_error', 1, data.pin, data.state)
        raise HTTPException(status_code=400, detail="Неверная команда")
    return {"status": device_state.get_status(data.pin)}


@router.post("/1/mode")
async def set_mode(data: ModeData):
    if data.mode == "manual":
        await device.set_manual(data.pin)
    elif data.mode == "auto":
        pass  # логика авто-режима отдельно
    else:
        raise HTTPException(status_code=400, detail="Неверный режим")

    return {"status": "ok"}


@router.post("/1/schedule")
async def set_schedule(data: ScheduleData):
    await device.set_state(data.pin, 0)
    await device.set_schedule(data.pin, data.on_time, data.off_time)
    return {"status": "ok"}


@router.get("/1/pin-status")
async def get_status():
    return {"pins": device_state.export_all_statuses()}

@router.get("/1/full-status")
async def get_full_status():
    pins = {}

    # берём все пины, по которым хоть что-то установлено
    all_pins = set(device_state.pin_modes.keys()) | set(device_state.pin_status.keys()) | set(device_state.pin_schedule.keys())

    for pin in sorted(all_pins):
        pins[pin] = {
            "state": device_state.get_status(pin),
            "mode": device_state.get_mode(pin),
            "schedule": device_state.get_schedule(pin) or None
        }
    print(pins)
    return {"pins": pins}