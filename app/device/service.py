from fastapi import WebSocket, HTTPException, status

from app.ws.manager import ws_manager


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
