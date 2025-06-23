import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.config import LoggingSettings, HOST, WS_PROTOCOL, DEVICE_RUN
from device_client.main import run_device
from telegram_client.bot import run_telegram_bot
from app.interface.device.routers import router as device_rt
from app.interface.web.routers import router as web_interface_rt
from app.infrastructure.logger_module.config import LoggingConfig
from app.infrastructure.devices.redis_state import device_state

settings = LoggingSettings()  # прочитает .env автоматически
LoggingConfig(settings).setup()


def get_logger(name: str = __name__) -> logging.Logger:
    return logging.getLogger(name)


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    loop.create_task(run_telegram_bot())
    if DEVICE_RUN:
        loop.create_task(run_device())
    await device_state.preload()
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="web_client"), name="static")
app.include_router(device_rt)
app.include_router(web_interface_rt)
templates = Jinja2Templates(directory='web_client')


@app.get('/', response_class=HTMLResponse)
async def welcome(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'host': HOST, 'ws_protocol': WS_PROTOCOL})
