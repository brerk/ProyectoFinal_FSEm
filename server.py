from fastapi import FastAPI, Form, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import random
import time

from loguru import logger
from typing import Annotated, List
from datetime import datetime

from models.RiegoModel import RiegoConfig
from utils.PID import PID

# CONSTANTS
from utils.database import db

# from utils.DS18B20_Sensor import S0, S1
from utils.PID import PID

scheduler = AsyncIOScheduler(timezone="America/Mexico_City")

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class LightControl(BaseModel):
    value: int


class FanSpeed(BaseModel):
    value: int


LIGHT_PWR = 10
FAN_SPEED = 50

MIN_TEMP = 20
MAX_TEMP = 25


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

    # TODO: save to database

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

    # TODO: save to database

    return {"fan_speed": FAN_SPEED}


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


@app.post("/temps_form")
def handle_temps_config(
    request: Request,
    min_temp: Annotated[float, Form()],
    max_temp: Annotated[float, Form()],
):
    global MIN_TEMP
    global MAX_TEMP

    print(f"{min_temp=} {max_temp=}")

    db.set_temp_limits(min_temp, max_temp)

    MIN_TEMP = min_temp
    MAX_TEMP = max_temp

    response = RedirectResponse(url="/")
    response.status_code = status.HTTP_303_SEE_OTHER

    return response


# Always at the end
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return get_template(request, "main")


def init_manager():
    """
    Init secuence, load config to memory and creates graphics if enought data is stored
    """
    global MIN_TEMP, MAX_TEMP
    temps = db.get_temp_limits()

    if not temps:
        MIN_TEMP = 20
        MAX_TEMP = 28
    else:
        MIN_TEMP = temps[0]["min_temp"]
        MAX_TEMP = temps[0]["max_temp"]

    # TODO: Load routines to scheduler
    # Create graphs

    # for _ in range(10):
    #     db.add_temperature_record(sensor_id=0, temp=random.random() * 100)
    #     time.sleep(1)
    #
    # for _ in range(10):
    #     db.add_temperature_record(sensor_id=1, temp=random.random() * 100)
    #     time.sleep(1)

    """
    Pasos para ajustar valores

    Kp:
        respuesta es lenta, aumenta Kp
        respuesta es rapida y oscila, reduce Kp

    Ki:
        error estable (temp doesn't reach setpoint), aumenta Ki
        respuesta inestable, reduce Ki

    Kd:
        oscilaciones rapida, aumenta Kd
        respuesta muy lenta, reduce Kd
    """

    # TODO: K constanst can be calculated automatically from measurements

    Kp = 2.0
    Ki = 0.1
    Kd = 1.0
    setpoint = 25.0  # Temperatura deseada en grados Celsius
    # measurement = 20.0  #

    for temp_reg in db.get_temperatures(0):
        # print(temp_reg)
        pid_res = PID(Kp, Ki, Kd, setpoint, temp_reg["temp"])

        print(f"PID: {pid_res} for {temp_reg["temp"]} --> wanted {setpoint}")

        # input()

    # for temp_reg in db.get_temperatures(1):
    #     print(temp_reg)


def get_existing_tasks() -> List[RiegoConfig]:
    """
    Load existing tasks from DataBase.
    """
    # TODO: Load data from database

    tasks = db.get_irrigation_tasks()
    # print(tasks)

    return tasks


def get_template(request, name: str):
    """
    Get jinja2 template
    """
    match name:
        case "main":
            return templates.TemplateResponse(
                request=request,
                name="index.html",
                context={
                    "fan_speed": FAN_SPEED,
                    "light_percentage": LIGHT_PWR,
                    "existing_task": get_existing_tasks(),
                    "curr_min_temp": MIN_TEMP,
                    "curr_max_temp": MAX_TEMP,
                },
            )

        case _:
            return None


def start_irrigation_routine(
    hourminute: str,
    duration: int,
    min_temp: float,
    max_temp: float,
):
    # TODO: Check temps limits
    # TODO: Start irrigation until duration is done

    pass


init_manager()
