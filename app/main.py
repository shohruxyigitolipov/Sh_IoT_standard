import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import LoggingSettings
from app.device.routers import router as device_rt
from app.logger_module.config import LoggingConfig

settings = LoggingSettings()  # прочитает .env автоматически
LoggingConfig(settings).setup()


def get_logger(name: str = __name__) -> logging.Logger:
    return logging.getLogger(name)


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.events import handles
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(device_rt)


@app.get('/')
async def welcome():
    return {"message": "Hello, world!"}
