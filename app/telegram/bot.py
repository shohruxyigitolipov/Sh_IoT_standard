from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from app.config import BOT_TOKEN
import pytz
from datetime import datetime

from app.telegram.routers import user_rt

default = DefaultBotProperties(parse_mode='MARKDOWN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def setup_routers():
    dp.include_router(user_rt)


def setup_timezone():
    pytz.timezone("Asia/Tashkent")
    datetime.now().replace(tzinfo=pytz.utc)


async def run_telegram_bot():
    setup_routers()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
