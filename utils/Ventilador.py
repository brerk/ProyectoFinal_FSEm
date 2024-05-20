import RPi.GPIO as GPIO
import time

# Configuración de los pines GPIO
GPIO.setmode(GPIO.BCM)
MOTOR_PIN = 18  # Pin GPIO al que está conectado el motor

GPIO.setup(MOTOR_PIN, GPIO.OUT)

# Configuración de PWM en el pin
pwm = GPIO.PWM(MOTOR_PIN, 100)  # Frecuencia de 100 Hz
pwm.start(0)  # Comienza con un ciclo de trabajo del 0%


def aumentar_velocidad(velocidad_actual, incremento):
    nueva_velocidad = min(100, velocidad_actual + incremento)
    pwm.ChangeDutyCycle(nueva_velocidad)
    print(f"Velocidad aumentada a {nueva_velocidad}%")
    return nueva_velocidad


def disminuir_velocidad(velocidad_actual, decremento):
    nueva_velocidad = max(0, velocidad_actual - decremento)
    pwm.ChangeDutyCycle(nueva_velocidad)
    print(f"Velocidad disminuida a {nueva_velocidad}%")
    return nueva_velocidad


try:
    velocidad = 0  # Velocidad inicial
    incremento = 10  # Incremento y decremento de la velocidad

    while True:
        comando = (
            input(
                "Ingrese 'a' para aumentar la velocidad, 'd' para disminuir la velocidad, o 'q' para salir: "
            )
            .strip()
            .lower()
        )

        if comando == "a":
            velocidad = aumentar_velocidad(velocidad, incremento)
        elif comando == "d":
            velocidad = disminuir_velocidad(velocidad, decremento)
        elif comando == "q":
            break
        else:
            print("Comando no reconocido. Intente de nuevo.")

except KeyboardInterrupt:
    print("Programa terminado por el usuario")
finally:
    pwm.stop()  # Detener PWM
    GPIO.cleanup()  # Limpiar la configuración de GPIO
