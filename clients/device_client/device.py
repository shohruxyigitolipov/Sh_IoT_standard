import asyncio
import datetime
import json
from typing import Literal, Dict, cast

from .logger_config import get_logger

logger = get_logger("device_client")

PinMode = Literal["manual", "auto"]
PinState = Literal[1, 0]
const_pins = [4, 5, 15, 16, 17, 18, 21, 22, 23]
pins_config = {i: {'mode': 'manual', 'state': 0} for i in const_pins}


class DeviceImitator:
    def __init__(self):
        self.ws = None
        self.pin_modes: Dict[int, PinMode] = {}
        self.pin_status: Dict[int, PinState] = {}
        self.pin_schedule: Dict[int, Dict[str, str]] = {}
        self.pin_names: Dict[int, str] = {}

        for pin, cfg in pins_config.items():
            self.pin_modes[pin] = cast(PinMode, cfg["mode"])
            self.pin_status[pin] = cast(PinState, cfg["state"])
        for pin in const_pins:
            self.pin_schedule[pin] = {'on_time': '12:00', 'off_time': '13:00'}
        logger.info(f"Initial pin schedule: {self.pin_schedule}")

    async def set_ws(self, websocket):
        self.ws = websocket
        logger.info("WebSocket connection established")

    async def report_to(self, pin: int = None):
        if not pin:
            pin_list = []
            for pin in const_pins:
                pin_list.append(pin)
        else:
            pin_list = [pin]
        report_data = []
        for pin in pin_list:
            data = {
                'pin': pin,
                'state': self.pin_status.get(pin),
                'mode': self.pin_modes.get(pin),
                'schedule': self.pin_schedule.get(pin),
                'name': self.pin_names.get(pin)
            }
            report_data.append(data)
        payload = {'type': 'report', 'pin_list': report_data}
        logger.info(f"Sending report: {payload}")
        await self.ws.send(json.dumps(payload))

    async def set_mode(self, pin: int, mode: PinMode):
        self.pin_modes[pin] = mode
        logger.info(f"Mode for pin {pin} set to {mode}")
        await self.report_to(pin)

    async def set_state(self, pin: int, state: PinState):
        self.pin_status[pin] = state
        logger.info(f"State for pin {pin} set to {state}")
        await self.report_to(pin)

    async def set_schedule(self, pin: int, on_time: str, off_time: str):
        self.pin_schedule[pin] = {"on_time": on_time, "off_time": off_time}
        logger.info(
            f"Schedule for pin {pin} updated: on_time={on_time}, off_time={off_time}"
        )
        await self.report_to(pin)

    async def set_name(self, pin: int, name: str | None):
        if name:
            self.pin_names[pin] = name
            logger.info(f"Name for pin {pin} set to {name}")
        else:
            self.pin_names.pop(pin, None)
            logger.info(f"Name for pin {pin} cleared")
        await self.report_to(pin)

    async def run_schedule(self, period: Literal[30, 60]):
        logger.info('Scheduler started')
        while True:
            gmt_plus_5 = datetime.timezone(datetime.timedelta(hours=5))
            now = datetime.datetime.now(gmt_plus_5).time()
            for pin in const_pins:
                if self.pin_modes[pin] != 'auto':
                    continue

                time_cfg = self.pin_schedule[pin]
                on_time_str = time_cfg.get('on_time')  # '12:00'
                off_time_str = time_cfg.get('off_time')  # '13:00'
                if on_time_str and off_time_str:
                    on_time = datetime.datetime.strptime(on_time_str, "%H:%M").time()
                    off_time = datetime.datetime.strptime(off_time_str, "%H:%M").time()

                    if on_time < off_time:
                        # обычный интервал: например, 12:00 - 13:00
                        is_on = on_time <= now < off_time
                    else:
                        # ночной интервал: например, 22:00 - 06:00
                        is_on = now >= on_time or now < off_time

                    self.pin_status[pin] = 1 if is_on else 0
                    await self.report_to(pin)
                    logger.info(
                        f'Now: {now} | on_time: {on_time} | off_time: {off_time}'
                    )
                    logger.info(f'Pin {pin} state in schedule: {is_on}')
            await asyncio.sleep(period)

    async def start(self):
        asyncio.create_task(self.run_schedule(period=30))
