from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.telegram.keyboards.device_keyboards import main_kb

user_rt = Router(name='users')


@user_rt.message(Command('start'))
async def handle_start(msg: Message):
    await msg.answer('Привет', reply_markup=main_kb())

