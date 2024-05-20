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


if __name__ == "__main__":
    for _ in range(10):
        db.add_temperature_record(sensor_id=0, temp=random.random() * 100)

    for _ in range(10):
        db.add_temperature_record(sensor_id=1, temp=random.random() * 100)
