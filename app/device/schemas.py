from pydantic import BaseModel, constr, Field
from datetime import datetime


class DeviceStatus_response(BaseModel):
    device_id: int
    status: bool


class Device(BaseModel):
    device_id: int


class CommandResponse(Device):
    success: bool
    command: str


class ErrorResponse(BaseModel):
    error: str


class PinAction(BaseModel):
    pin: int = Field(..., ge=0, le=39)
    state: int


class ScheduleData(BaseModel):
    pin: int
    on_time: str  # "08:00"
    off_time: str  # "20:00"


class ModeData(BaseModel):
    pin: int
    mode: str  # "manual" | "auto"
