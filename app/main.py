import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.config.config import LoggingSettings
from app.telegram.bot import run_telegram_bot
from interface.device.routers import router as device_rt
from interface.web.routers import router as web_interface_rt
from infrastructure.logger_module.config import LoggingConfig

settings = LoggingSettings()  # прочитает .env автоматически
LoggingConfig(settings).setup()


def get_logger(name: str = __name__) -> logging.Logger:
    return logging.getLogger(name)


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.infrastructure.devices import event_handlers as device_event
    from app.infrastructure.devices import event_loggers as device_log
    from app.infrastructure.web_interface import event_loggers as web_log
    from app.infrastructure.web_interface import event_handlers as web_event
    loop = asyncio.get_event_loop()

    loop.create_task(run_telegram_bot())
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/webapp"), name="static")
app.include_router(device_rt)
app.include_router(web_interface_rt)
templates = Jinja2Templates(directory="app/templates")
templates2 = Jinja2Templates(directory='app/webapp')

@app.get('/', response_class=HTMLResponse)
async def welcome(request: Request):
    return templates2.TemplateResponse('index.html', {'request': request})


@app.get('/test', response_class=HTMLResponse)
async def test(request: Request):
    return templates.TemplateResponse('gpio_control_panel_v2.html', {'request': request})
