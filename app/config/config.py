import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pyee.asyncio import AsyncIOEventEmitter

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # config/ -> app/ -> проект
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
url = os.getenv('PUBLIC_HOST')
event_bus = AsyncIOEventEmitter()

PinMode = Literal["manual", "auto"]
PinState = Literal[1, 0]
const_pins = [4, 5, 15, 16, 17, 18, 21, 22, 23]
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
    formatter: str = "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s"
    telegram_formatter: str = "[%(levelname)s] %(name)s:%(lineno)d\n%(message)s"
    model_config = SettingsConfigDict(
        env_file="../../.env",  # путь до вашего .env
        env_file_encoding="utf-8",  # кодировка .env
        extra='ignore'
    )
