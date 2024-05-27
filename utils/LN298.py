import RPi.GPIO as GPIO          
from time import sleep

"""
motor 0 ventilador pwm
motor 1 bomba de agua gpio
"""

#pines para el primer motor
in1 = 24
in2 = 23
en1 = 25

#pines para el primer motor
in3 = 14
in4 = 15
en2 = 18

GPIO.setmode(GPIO.BCM)

class LD298_Driver:
    def __init__(self) -> None:
        #Configuración de pines del primer motor ventilador
        GPIO.setup(in1, GPIO.OUT)
        GPIO.setup(in2, GPIO.OUT)
        GPIO.setup(en1, GPIO.OUT)
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)

        self.fan=GPIO.PWM(en1, 1000)

        #Configuración de pines del primer motor waterpump
        GPIO.setup(in3, GPIO.OUT)
        GPIO.setup(in4, GPIO.OUT)
        GPIO.setup(en2, GPIO.OUT)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.LOW)

        self.waterpump=GPIO.PWM(en2, 1000)

        self.fan.start(25)
        self.waterpump.start(25)

    def motor_on(self, motor_id: str):
        if motor_id == "pump":
            GPIO.output(in3,GPIO.HIGH)
            GPIO.output(in4,GPIO.LOW)
        elif motor_id == "fan":
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
        else:
            print(f"Option {motor_id} not valid.")

    def motor_off(self, motor_id: str):
        if motor_id == "pump":
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)
        elif motor_id == "fan":
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.LOW)
        else:
            print(f"Option {motor_id} not valid.")

    def set_fan_speed(self, speed: int):
        if speed > 100 or speed < 0:
            print(f"Speed {speed} is not valid.")
            return

        self.fan.ChangeDutyCycle(speed)


motors = LD298_Driver()
