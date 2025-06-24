from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram_client.logger_config import get_logger

logger = get_logger()

user_rt = Router(name='users')
url = f"https://shiotstandard-production.up.railway.app"


def main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Панель управления', web_app=WebAppInfo(url=url))],
        [InlineKeyboardButton(text='Помощь', callback_data='devices-help')],
    ])

@user_rt.message(Command('start'))
async def handle_start(msg: Message):
    logger.info(f"/start from {msg.from_user.id}")
    await msg.answer('Привет', reply_markup=main_kb())

