from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime

from app.telegram.keyboards.time_keyboard import time_kb


def highlight_cursor(text: str, cursor: int) -> str:
    if 0 <= cursor < len(text):
        return text[:cursor] + '\u0332' + text[cursor] + text[cursor + 1:]
    return text


async def handle_time_input(call: CallbackQuery, state: FSMContext):
    value, cursor, device_id, device_type = call.data.replace('time,', '').split(',')
    cursor = int(cursor)
    data = await state.get_data()
    time_string = data.get("edit_time", "00:00–00:00")
    time_list = list(time_string)

    if value == '*':
        while cursor > 0 and time_list[cursor] in {':', '–'}:
            cursor -= 1
        time_list[cursor] = '0'
        next_cursor = max(0, cursor - 1)

    elif value == 'submit':
        start, stop = ''.join(time_list[0:5]), ''.join(time_list[6:11])
        try:
            if datetime.strptime(start, "%H:%M") >= datetime.strptime(stop, "%H:%M"):
                await call.answer("Время выключения должно быть позже включения", show_alert=True)
                return
        except:
            await call.answer("Ошибка формата времени", show_alert=True)
            return
        await call.message.edit_text(f"Время включения: {start}\nВремя выключения: {stop}")
        return start, stop, device_id, device_type

    else:
        if time_list[cursor] in {':', '–'}:
            cursor += 1
        time_list[cursor] = value
        next_cursor = cursor + 1
        while next_cursor < len(time_list) and time_list[next_cursor] in {':', '–'}:
            next_cursor += 1

    new_time_string = ''.join(time_list)
    await state.update_data(edit_time=new_time_string)
    highlighted = highlight_cursor(new_time_string, next_cursor)
    await call.message.edit_text(
        text=f"Установите время:\n{highlighted}",
        reply_markup=await time_kb(device_id=int(device_id), device_type=device_type, cursor=next_cursor)
    )
