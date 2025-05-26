from app.device.repository import DeviceRepository
from app.db.service import BaseService
from fastapi import WebSocket, HTTPException, status

from app.device.adapters import DeviceCommands
from app.ws.manager import ws_manager


class DeviceService(BaseService[DeviceRepository]):
    def __init__(self, repo: DeviceRepository):
        """
        Сервис для работы с устройствами, содержащий как методы, связанные с базой данных,
        так и управляющие действия через WebSocket.

        :param repo: Репозиторий для работы с таблицей устройств.
        """
        super().__init__(repo)

    async def list_all(self):
        """
        Получить все устройства из базы данных.

        :return: Список всех устройств.
        """
        return await self.repo.get_all_devices()

    async def list_filtered_sorted(self, name: str = None, sort: str = None):
        """
        Получить устройства с фильтрацией по имени и сортировкой.

        :param name: Фильтр по имени устройства.
        :param sort: Поле сортировки.
        :return: Список отфильтрованных и отсортированных устройств.
        """
        return await self.repo.get_filtered_sorted(name=name, sort=sort)

    @staticmethod
    async def get_websocket_or_404(device_id: int) -> WebSocket:
        """
        Получить активное WebSocket-соединение устройства, или вернуть 404, если соединение отсутствует.

        :param device_id: Идентификатор устройства.
        :return: WebSocket-объект.
        :raises HTTPException: Если соединение отсутствует.
        """
        session = await ws_manager.get(device_id)
        websocket = session.websocket
        if not websocket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Устройство {device_id} не подключено.'
            )
        return websocket

    @staticmethod
    async def control_device(device_id: int, get_status: bool = False, state: bool = None,
                             start_time: str = None, stop_time: str = None):
        """
        Управлять устройством через WebSocket.

        Поддерживает:
        - установку таймера (start_time и stop_time)
        - включение/выключение устройства (state)
        - очистку таймера

        :param device_id: ID устройства.
        :param get_status: Запрос состояния.
        :param state: Целевое состояние (вкл/выкл).
        :param start_time: Время включения.
        :param stop_time: Время выключения.
        :return: Результат действия и текущее состояние.
        """

        device = DeviceCommands(device_id=device_id)
        if get_status:
            response = await device.get_status()
            return response
        if start_time and stop_time:
            response = await device.set_timer(start_time=start_time, stop_time=stop_time)
            return response
        if state is not None:
            response = await device.set_state(state=state)
            return response

        response = await device.clear_timer()
        return response

    @staticmethod
    async def get_device_status(device_id: int) -> bool:
        """
        Получить текущее состояние устройства через WebSocket.

        :param device_id: Идентификатор устройства.
        :param device_type: Тип устройства.
        :return: True — включено, False — выключено.
        """
        websocket = await DeviceService.get_websocket_or_404(device_id)
        device = DeviceCommands(device_id=device_id)
        return await device.get_state()

    async def verify_auth_token(self, device_id: int, auth_token: str):
        device = await self.repo.get_by_auth_token(auth_token=auth_token)
        if device and device.id == device_id:
            return True
        return False
