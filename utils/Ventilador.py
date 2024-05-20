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
            print("speed is not on limits")
            return

        self.pwm.ChangeDutyCycle(speed)
        print("pwm values changed to: ", speed)


fan = Fan()

if __name__ == "__main__":
    while True:
        speed = input("Input speed: ")
        fan.set_speed(int(speed))
