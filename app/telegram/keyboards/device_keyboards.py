from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


def main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Мои устройства', callback_data='my-devices')],
        [InlineKeyboardButton(text='Добавить устройство', callback_data='add-device')],
        [InlineKeyboardButton(text='Помощь', callback_data='devices-help')],
        [InlineKeyboardButton(text='Панель управления', web_app=WebAppInfo(url='https://shiot-production.up.railway.app'))]
    ])


def manage_device_kb(device_id: int, device_type: str, status: bool | int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Включить', callback_data=f'control-device,{device_id},{device_type},turn_on')],
        [InlineKeyboardButton(text='Выключить', callback_data=f'control-device,{device_id},{device_type},turn_off')],
        [InlineKeyboardButton(text='Настроить таймер',
                              callback_data=f'control-device,{device_id},{device_type},set_timer')],
        [InlineKeyboardButton(text='Выключить таймер',
                              callback_data=f'control-device,{device_id},{device_type},clear_timer')],
    ])


async def devices_kb() -> InlineKeyboardMarkup | None:
    devices = await DeviceService.get_devices()
    if not devices:
        return None

    buttons = []
    for device in devices:
        status = await DeviceService.get_device_status(device['id'])
        symbol = '🟢' if status else '⚫'
        btn = InlineKeyboardButton(
            text=f"{device['name']}:{symbol}",
            callback_data=f"devices-{device['name']},{device['id']}"
        )
        buttons.append(btn)

    inline = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    return InlineKeyboardMarkup(inline_keyboard=inline)
