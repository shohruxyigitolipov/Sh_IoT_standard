import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.config import LoggingSettings, HOST, WS_PROTOCOL
from app.interface.device.routers import router as device_rt
from app.interface.web.routers import router as web_interface_rt
from app.infrastructure.logger_module.config import LoggingConfig
from app.infrastructure.logger_module.utils import get_logger_factory
from app.application.devices.redis_state import device_state

settings = LoggingSettings()  # прочитает .env автоматически
LoggingConfig(settings).setup()

get_logger = get_logger_factory("server")
logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Server starting")
    await device_state.preload()
    try:
        yield
    finally:
        logger.info("Server stopped")


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="web_client"), name="static")
app.include_router(device_rt)
app.include_router(web_interface_rt)
templates = Jinja2Templates(directory='web_client')


@app.get('/', response_class=HTMLResponse)
async def welcome(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'host': HOST, 'ws_protocol': WS_PROTOCOL})
