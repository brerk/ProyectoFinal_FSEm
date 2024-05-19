import RPi.GPIO as GPIO
import schedule
import time
from datetime import datetime

# Configuración de los pines GPIO
GPIO.setmode(GPIO.BCM)
BombaAgua_PIN_10_MIN = 17  # Pin GPIO para BombaAgua que se enciende cada 10 minutos
BombaAgua_LED_PIN_10_AM = 27   # Pin GPIO para el BombaAgua que se enciende a las 10 AM

GPIO.setup(BombaAgua_PIN_10_MIN, GPIO.OUT)
GPIO.setup(BombaAgua_PIN_10_AM, GPIO.OUT)

def encender_led_10_min():
    print(f"Encendiendo LED de 10 minutos a las {datetime.now()}")
    GPIO.output(BombaAgua_PIN_10_MIN, GPIO.HIGH)
    time.sleep(5)  # Mantener el BombaAgua encendido por 5 segundo
    GPIO.output(BombaAgua_PIN_10_MIN, GPIO.LOW)

def encender_led_10_am():
    print(f"Encendiendo LED de las 10 AM a las {datetime.now()}")
    GPIO.output(BombaAgua_PIN_10_AM, GPIO.HIGH)
    time.sleep(5)  # Mantener el LED encendido por 5 segundo
    GPIO.output(BombaAgua_PIN_10_AM, GPIO.LOW)

# Programar las tareas
schedule.every(10).minutes.do(encender_led_10_min)
schedule.every().day.at("10:00").do(encender_led_10_am)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)  # Esperar un segundo antes de verificar las tareas nuevamente
except KeyboardInterrupt:
    print("Programa terminado por el usuario")
finally:
    GPIO.cleanup()  # Limpiar la configuración de GPIO
