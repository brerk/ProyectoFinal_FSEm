# PID Controls the light power using Proportional gain + integral gain + derivative gain to keep temperature on setpoint
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


import time
import random
from utils.database import db

integral = 0
# time_prev = -1e-6
time_prev = None
e_prev = 0


def PID(Kp, Ki, Kd, setpoint: float, measurement: float, offset=5) -> float:
    """
    Kp: Proportional gain
    Ki: Integral gain
    Kd: Derivative gain
    setpoint: Wanted temperature in Celsius
    measurement: Current temperature
    offset: Base value for the output (default 5)

    Proportional-Integral-Derivative Controller

    Control of a heavy load power usage trought a PID in a scale of 0 --> 100%.

    Consist of 3 parts

    - Kp * error
    - Ki * integral --> eliminate the offset
    - Kd * differential --> faster response

    The PID receives: current temperature (s0, s1), calculates error and depending of it, controls the light.

    This implementation uses a discrete aproach, where the integral is calculated as increments
    """

    global integral, time_prev, e_prev

    # PID calculations
    current_time = time.time()

    if not time_prev:
        time_prev = current_time

    dt = current_time - time_prev
    print(f"{dt=} {current_time=} {time_prev=}")

    if dt <= 0:
        dt = 1e-16  # Avoid division by 0

    e = setpoint - measurement

    print(f"{e=}")

    # PID calculations
    P = Kp * e
    print(f"{P=}")

    integral += e * dt
    I = Ki * integral
    print(f"{I=}")

    D = Kd * (e - e_prev) / dt
    print(f"{D=}")

    MV = offset + P + I + D
    print(MV)
    MV = max(0, min(100, MV))

    e_prev = e
    time_prev = current_time

    return MV


def fill_db_with_fake_measurements():
    for _ in range(10):
        db.add_temperature_record(sensor_id=0, temp=random.random() * 100)

    for _ in range(10):
        db.add_temperature_record(sensor_id=1, temp=random.random() * 100)


if __name__ == "__main__":
    fill_db_with_fake_measurements()

    Kp = 2.0
    Ki = 0.1
    Kd = 1.0
    setpoint = 25.0  # Temperatura deseada en grados Celsius
    measurement = 20.0  #

    pid_res = PID(Kp, Ki, Kd, setpoint, measurement)

    print(f"PID result -> {pid_res}")
