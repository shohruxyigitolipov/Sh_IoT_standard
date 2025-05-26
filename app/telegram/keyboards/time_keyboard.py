from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def time_kb(device_id: int, device_type: str, cursor: int = 0) -> InlineKeyboardMarkup:
    digits = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    keyboard = [
        [InlineKeyboardButton(text=str(n), callback_data=f'time,{n},{cursor},{device_id},{device_type}') for n in row]
        for row in digits
    ]
    keyboard.append([
        InlineKeyboardButton(text='0', callback_data=f'time,0,{cursor},{device_id},{device_type}'),
        InlineKeyboardButton(text='🔙', callback_data=f'time,*,{cursor},{device_id},{device_type}'),
        InlineKeyboardButton(text='✅', callback_data=f'time,submit,{cursor},{device_id},{device_type}')
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
