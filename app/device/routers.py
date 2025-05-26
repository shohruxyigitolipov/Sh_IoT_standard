from fastapi import HTTPException
from typing import List

from fastapi import APIRouter, Query, WebSocket, Depends

from app.device.dependencies import get_device_service
from app.device.service import DeviceService
from app.device.schemas import *
from app.events.emitters import event_bus
from app.logger_module.utils import get_logger_factory
from app.ws.manager import ws_manager
from app.ws.handler import ws_handler as websocket_handler

get_logger = get_logger_factory(__name__)
logger = get_logger()

router = APIRouter(prefix='/devices')


@router.websocket('/ws/{device_id}/connect')
async def websocket_connection(websocket: WebSocket, device_id: int,
                               service: DeviceService = Depends(get_device_service)):
    await websocket.accept()
    logger.info('⏳Установлена временная связь.\n'
                ' Ожидание дополнительных данных...')
    await websocket_handler.handle_connection(websocket=websocket, device_id=device_id, service=service)
    # {"auth_token": "abc123"}


@router.post(path='/control/{device_id}', response_model=DeviceControl_response, summary='Управление устройством')
async def control_socket(device_id: int, request: DeviceControl_request,
                         service: DeviceService = Depends(get_device_service)):
    response = await service.control_device(
        device_id=device_id,
        **request.model_dump()
    )

    return DeviceControl_response(response=response, device_id=device_id)


@router.get('/{device_id}/status', response_model=DeviceStatus_response)
async def get_device_status_r(device_id: int):
    devices = await ws_manager.get_list()
    return DeviceStatus_response(device_id=device_id, status=device_id in devices)


@router.get('/active', response_model=ActiveDevicesResponse, summary='Список активных устройств')
async def active_devices():
    device_ids = await ws_manager.get_list()
    return ActiveDevicesResponse(active_devices=device_ids)


@router.get('/all', response_model=List[DeviceInfo])
async def get_all_devices_in_short(service: DeviceService = Depends(get_device_service),
                                   name: str = Query(None), sort: str = Query(None)):
    devices = await service.list_filtered_sorted(name=name, sort=sort)
    return devices


@router.post('/create', response_model=DeviceInfo, response_model_exclude_none=True)
async def create_device(data: DeviceCreate, service: DeviceService = Depends(get_device_service)):
    try:
        device = await service.create(data)
        event_bus.emit('new_device', device.id)
        return device
    except Exception as e:
        logger.error(f'Ошибка при создании устройства: {e}')
        raise HTTPException(status_code=500, detail="Ошибка на сервере при создании устройства")

