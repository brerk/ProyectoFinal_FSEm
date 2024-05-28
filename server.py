# Smart Greenhouse using a raspberry pi 4 + arduino one + web interface
# Copyright (C) 2024  Erik Bravo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from fastapi import FastAPI, Form, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
import time

from loguru import logger
from typing import Annotated, List, Union

from models.RiegoModel import RiegoConfig
from utils.PID import PID
from utils.i2c_master import i2c_handler

# CONSTANTS
from utils.database import db
from utils.Graphs import create_temps_graph
from utils.LN298 import motors

scheduler = BackgroundScheduler(timezone="America/Mexico_City")

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class LightControl(BaseModel):
    value: int


class FanSpeed(BaseModel):
    value: int


LIGHT_PWR = 10
FAN_SPEED = 75

MIN_TEMP = 20
MAX_TEMP = 25

DESIRED_TEMP = 25

PID_CONSTANTS = {
    "kp": 1.0,
    "ki": 1*0.1,
    "kd": 1*0.1*0.1,
}


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

    pwr = (8000 * LIGHT_PWR) / 100

    print(f"Send: {pwr=}")

    i2c_handler.send_cmd("light", pwr)

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

    motors.motor_on("fan")
    motors.set_fan_speed(FAN_SPEED)

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

    hour, minute = hourminute.split(":")
    scheduler.add_job(
        start_irrigation_routine,
        "cron",
        hour=hour,
        minute=minute,
        id=f"irrigation_task_new_{hourminute}",
        args=(
            hourminute,
            duration,
            min_temp,
            max_temp,
        ),
    )

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

    db.set_temp_limits(min_temp, max_temp)

    MIN_TEMP = min_temp
    MAX_TEMP = max_temp

    response = RedirectResponse(url="/")
    response.status_code = status.HTTP_303_SEE_OTHER

    return response


@app.post("/wanted_temp_form")
def handle_wanted_temp(
    request: Request,
    wanted_temp: Annotated[float, Form()],
):
    global DESIRED_TEMP

    DESIRED_TEMP = wanted_temp

    response = RedirectResponse(url="/")
    response.status_code = status.HTTP_303_SEE_OTHER

    return response

@app.post("/pid_control")
def handle_pid_control(
    request: Request,
    kp: Annotated[float, Form()],
    ki: Annotated[float, Form()],
    kd: Annotated[float, Form()],
):
    global PID_CONSTANTS

    PID_CONSTANTS["kp"] = kp
    PID_CONSTANTS["ki"] = ki
    PID_CONSTANTS["kd"] = kd

    response = RedirectResponse(url="/")
    response.status_code = status.HTTP_303_SEE_OTHER

    return response



# Always at the end
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return get_template(request, "main")


def init_routine():
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

    s0_temps = db.get_temperatures(0)
    s1_temps = db.get_temperatures(1)

    create_temps_graph(s0_temps, s1_temps)

    tasks = db.get_irrigation_tasks()
    if tasks:
        for task in tasks:
            hour, minute = task.time.split(":")
            scheduler.add_job(
                start_irrigation_routine,
                "cron",
                hour=int(hour),
                minute=int(minute),
                id=f"irrigation_task_{task.id}",
                args=(
                    task.time,
                    task.duration,
                    task.min_temp,
                    task.max_temp,
                ),
            )


def get_existing_tasks() -> Union[List[RiegoConfig], None]:
    """
    Retrieve existing tasks from DataBase.
    """
    tasks = db.get_irrigation_tasks()

    if tasks:
        return tasks
    else:
        return None



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
                    "existing_task": get_existing_tasks() or [],
                    "curr_min_temp": MIN_TEMP,
                    "curr_max_temp": MAX_TEMP,
                    "wanted_temp": DESIRED_TEMP,
                    "curr_temp": f"{get_current_temp():.3f}",
                    "logs": db.get_logs(10),
                },
            )

        case _:
            return None

S0_TEMP = 0
S1_TEMP = 0


def get_current_temp() -> Union[float, None]:
    """
    Return prom of s0 + s1
    """
    global S0_TEMP, S1_TEMP

    # s0_temp = i2c_handler.read_temp_from_i2c(0)
    # s1_temp = i2c_handler.read_temp_from_i2c(1)

    s0_temp = S0_TEMP 
    s1_temp = S1_TEMP 

    print(f"{s0_temp=} {s1_temp=}")

    if s0_temp and s1_temp:
        temp_prom = (s0_temp + s1_temp)/2

        return temp_prom
    else:
        logger.warning("An error ocurreded while reading sensors.")
        return None


def start_irrigation_routine(
    hourminute: str,
    duration: int,
    min_temp: float,
    max_temp: float,
):
    curr_temp = get_current_temp()
    if not curr_temp:
        logger.warning(f"Could not get current_temp to excecute, skipping irrigation routine...")
        return

    if curr_temp < min_temp or curr_temp > max_temp:
        logger.info(
            f"Curr Temp {curr_temp} is not valid for temp limits {min_temp=} {max_temp=}, return."
        )
        return

    motors.motor_on("pump")
    logger.info("Started irrigation routine.")

    time.sleep(duration)

    motors.motor_off("pump")
    logger.info("Irrigation routine is done.")


@scheduler.scheduled_job("cron", second="*/2")
def control_light():
    """
    Adjust light power using the PID

    """

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
    current_temp = get_current_temp()

    if not current_temp:
        logger.warning("Could not get current temp for PID Adjustment, skipping.")
        return

    pid_res = PID(PID_CONSTANTS["kp"], PID_CONSTANTS["ki"], PID_CONSTANTS["kd"], DESIRED_TEMP, current_temp)


    pwr = 8000 - ((8000 * pid_res) / 100)

    if pwr < 0:
        pwr = 0
        print("reset pwr value")
    elif pwr > 100:
        pwr = 100
        print("lmitt pwr value to 100")


    i2c_handler.send_cmd("light", float(pwr))

    logger.info(f"PID: Adjust Light power to {pwr}/100 to reach {100-DESIRED_TEMP} C")


@scheduler.scheduled_job("cron", second="*/3")
def generate_graphs():
    s0_temps = db.get_temperatures(0)
    s1_temps = db.get_temperatures(1)

    if not s0_temps:
        logger.warning(f"No mesaurements saved for {s0_temps=}")
        return

    if not s1_temps:
        logger.warning(f"No mesaurements saved for {s1_temps=}")
        return

    create_temps_graph(s0_temps, s1_temps)

    db.add_log_row("Graph update", "Done")

    logger.info("Graphs updated to ./statics/temps.jpg")


@scheduler.scheduled_job("cron", second="*/1")
def measure_temps():
    """
    Read temperature from S0 y S0 and write to db.
    """

    global S0_TEMP, S1_TEMP

    s0_temp = i2c_handler.read_temp_from_i2c(0)
    s1_temp = i2c_handler.read_temp_from_i2c(1)

    S0_TEMP = s0_temp
    S1_TEMP = s1_temp

    if s0_temp is None or s1_temp is None or s1_temp == 0 or s0_temp ==0:  
        logger.warning(f"An error ocurred while reading temps from I2C: {s0_temp=} {s1_temp=}, skip measurement...")
        return

    db.add_temperature_record(sensor_id=0, temp=s0_temp)
    db.add_temperature_record(sensor_id=1, temp=s1_temp)

    db.add_log_row("Temp measurement of S0,S1", "Done")


scheduler.start()

init_routine()

motors.motor_on("fan")
motors.set_fan_speed(FAN_SPEED)
