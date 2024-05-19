from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from loguru import logger

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


class LightControl(BaseModel):
    value: int


class FanSpeed(BaseModel):
    value: int


LIGHT_PWR = 50
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


@app.post("/riego_config")
def handle_riego_config(data: RiegoConfig):
    # TODO: Add to datahase
    # Add job to scheduler
    # Confirm update

    pass


def init_routine():
    # Load routines to scheduler
    # Create graphs

    pass


# Always at the end
app.mount("/", StaticFiles(directory="static", html=True), name="static")
