import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.config import LoggingSettings
from app.device.routers import router as device_rt
from app.logger_module.config import LoggingConfig
from app.telegram.bot import run_telegram_bot

settings = LoggingSettings()  # прочитает .env автоматически
LoggingConfig(settings).setup()


def get_logger(name: str = __name__) -> logging.Logger:
    return logging.getLogger(name)


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.events import handles
    loop = asyncio.get_event_loop()
    loop.create_task(run_telegram_bot())
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(device_rt)
templates = Jinja2Templates(directory="app/templates")


@app.get('/', response_class=HTMLResponse)
async def welcome(request: Request):
    return templates.TemplateResponse('gpio_control_panel.html', {'request': request})

