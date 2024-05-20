import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
MOTOR_PIN = 18
GPIO.setup(MOTOR_PIN, GPIO.OUT)


class Fan:
    def __init__(self):
        self.pwm = GPIO.PWM(MOTOR_PIN, 100)  # Frecuencia de 100 Hz
        self.pwm.start(0)

    def set_speed(self, speed: int):
        if speed < 0 or speed > 100:
            return

        self.pwm.ChangeDutyCycle(speed)


fan = Fan()
