import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

WaterPump_PIN = 17

GPIO.setup(WaterPump_PIN, GPIO.OUT)


class WaterPump:
    def turn_on(self):
        GPIO.output(WaterPump_PIN, GPIO.HIGH)

    def turn_off(self):
        GPIO.output(WaterPump_PIN, GPIO.LOW)

    def discard(self):
        GPIO.cleanup()  # Limpiar la configuración de GPIO


wp = WaterPump()

if __name__ == "__main__":
    wp.turn_on()
