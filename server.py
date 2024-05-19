from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from pydantic import BaseModel
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from loguru import logger

from typing import Annotated
from datetime import datetime

from models.RiegoModel import RiegoConfig
from utils.database import db

"""
1. Encendido y apagado de sistema de irrigación.
2. Desplegado de gráfica con historico de temperatura, irrigación y acciones tomadas.
3. Control de temperatura del invernadero utilizando PID.
4. Control de potencia del radiador (foco incandecente).
5. Control de potencia de ventilador.
6. Programado de ciclos de temperatura e irrigado.
7. Servidor web para control.
"""

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


@app.post("/riego_form")
def handle_riego_config(
    request: Request,
    hourminute: Annotated[str, Form()],
    duration: Annotated[int, Form()],
    min_temp: Annotated[float, Form()],
    max_temp: Annotated[float, Form()],
):
    """
    /?hour-minute=12%3A12&duration=&min_temp=&max_temp= HTTP/1.1" 200 OK
    """

    # TODO: Add to datahase
    # Add job to scheduler
    # Confirm update

    print(f"{hourminute=}")
    print(f"{duration=}")
    print(f"{min_temp=}")
    print(f"{max_temp=}")

    if hourminute is None or duration is None or min_temp is None or max_temp is None:
        # Redirigir de vuelta al formulario con un mensaje de error
        logger.warning("No data was submitted")

    return get_template(request, "main")


def init_routine():
    # Load routines to scheduler
    # Create graphs

    pass


# Always at the end
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


def get_existing_tasks():
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
