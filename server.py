from fastapi import FastAPI, Form, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from loguru import logger
from typing import Annotated
from datetime import datetime

from models.RiegoModel import RiegoConfig

# CONSTANTS
from utils.database import db

# from utils.DS18B20_Sensor import S0, S1

scheduler = AsyncIOScheduler(timezone="America/Mexico_City")

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class LightControl(BaseModel):
    value: int


class FanSpeed(BaseModel):
    value: int


test_data = [
    RiegoConfig(
        time="10:20",
        duration=10,
        min_temp=20.0,
        max_temp=30.0,
        timestamp=datetime.now(),
    ),
    RiegoConfig(
        time="20:30",
        duration=10,
        min_temp=20.0,
        max_temp=30.0,
        timestamp=datetime.now(),
    ),
    RiegoConfig(
        time="23:30",
        duration=10,
        min_temp=20.0,
        max_temp=30.0,
        timestamp=datetime.now(),
    ),
]

LIGHT_PWR = 10
FAN_SPEED = 50


@app.post("/control_light")
def handle_light_power_change(control: LightControl):
    """
    Handle user click on button Light Toggle
    """
    global LIGHT_PWR

    if control.value is None:
        logger.warning(f"Value: {control.value} is not valid.")
        return

    logger.debug(f"Set light power to {control.value}")

    LIGHT_PWR = control.value

    return {"light_power": LIGHT_PWR}


@app.post("/control_fan")
def handle_fan_power_change(control: FanSpeed):
    """
    Handle user click on button Light Toggle
    """
    global FAN_SPEED

    if control.value is None:
        logger.warning(f"Value: {control.value} is not valid.")
        return

    logger.debug(f"Set fan speed to {control.value}")

    FAN_SPEED = control.value

    return {"fan_speed": FAN_SPEED}


def start_irrigation_routine(
    hourminute: str,
    duration: int,
    min_temp: float,
    max_temp: float,
):

    # TODO: Check temps limits
    # TODO: Start irrigation until duration is done

    pass


@app.post("/riego_form")
def handle_riego_config(
    request: Request,
    hourminute: Annotated[str, Form()],
    duration: Annotated[int, Form()],
    min_temp: Annotated[float, Form()],
    max_temp: Annotated[float, Form()],
):
    db.add_irrigation_set(
        hourminute,
        duration,
        min_temp,
        max_temp,
    )

    # TODO: Add job to scheduler

    # Don't stay on /riego_form, return to /
    response = RedirectResponse(url="/")
    response.status_code = status.HTTP_303_SEE_OTHER

    return response


def init_routine():
    # Load routines to scheduler
    # Create graphs

    pass


# Always at the end
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


def get_existing_tasks():
    # TODO: Load data from database
    return test_data


def get_template(request, name: str):
    match name:
        case "main":
            return templates.TemplateResponse(
                request=request,
                name="index.html",
                context={
                    "fan_speed": FAN_SPEED,
                    "light_percentage": LIGHT_PWR,
                    "existing_task": get_existing_tasks(),
                },
            )

        case _:
            return None


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return get_template(request, "main")
