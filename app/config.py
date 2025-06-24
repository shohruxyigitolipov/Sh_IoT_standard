import os
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pyee.asyncio import AsyncIOEventEmitter

load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
HOST = os.getenv('HOST')
WS_PROTOCOL = os.getenv('WS_PROTOCOL')
DEVICE_RUN = bool(os.getenv('DEVICE_RUN', 'false').lower() == 'true')
REDIS_URL = os.getenv('REDIS_URL')
event_bus = AsyncIOEventEmitter()

PinMode = Literal["manual", "auto"]
PinState = Literal[1, 0]

const_pins = list(map(int, os.getenv('PINS').split(',')))
pins_config = {i: {'mode': 'manual', 'state': 0} for i in const_pins}


# Настройка логирования

class LoggingSettings(BaseSettings):
    telegram_enabled: bool = True
    telegram_log_bot_token: str = ""
    telegram_chat_id: str = ""
    level: str = "INFO"
    log_to_console: bool = True
    log_to_file: bool = False
    log_file_path: str = "logs/app.log"
    max_bytes: int = 5 * 1024 * 1024
    backup_count: int = 3
    formatter: str = "[%(asctime)s] [server] [%(levelname)s] %(message)s (%(filename)s:%(lineno)d)"
    telegram_formatter: str = "[%(levelname)s] [server] %(message)s (%(filename)s:%(lineno)d)"
    model_config = SettingsConfigDict(
        env_file="../.env",  # путь до вашего .env
        env_file_encoding="utf-8",  # кодировка .env
        extra='ignore'
    )
