from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

user_rt = Router(name='users')

url = f"wss://shiotstandard-production.up.railway.app"


def main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Панель управления', web_app=WebAppInfo(url=url))],
        [InlineKeyboardButton(text='Помощь', callback_data='devices-help')],
    ])

@user_rt.message(Command('start'))
async def handle_start(msg: Message):
    await msg.answer('Привет', reply_markup=main_kb())

