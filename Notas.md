

# Entregables
##  Tutorial de elaboración (memoria tecnica)

Elaborado sumiendo que el lector no está familiarizado con la teoria de sistemas embebidos.

Debe guiar paso a paso en la implementación de una solución práctica desde el alambrado, conexión con el
microcontrolador, configuración de la tarjeta.

### Estructua

Objetivo
Lista de materiales
Descripción del funcionamiento
Adevertencias de uso
Cuidado de los componentes
Configuración de la tarjeta controladora, circuito, puertos, paquetes, bibliotecas a instalar, etcetera.
Desarrollo de los componentes (modulos) de python
Integración
Conclusiones
Cuestionario
Bibliografia

**SIN CARATULA**

## Prototipo funcional
## Video evidencia

## Repositorio y código fuente

Publico

Script de bash que automatize todo

Archivos de código fuente deben estar documentados con nombre del autor y licencia original.


# Opciones de proyecto
## Centro Multimedia

1. Asistente para conectarse a internet (bash)
2. Menú al encender que permite elegir entre que sitio mostrar (netflix, hbo, amazon, etc) o reproducir medio extraible
3. reproducir media desd la USB (foto y/o video)
4. Soporte para control remoto (apuntador y teclado en pantalla es aceptable pero no recomendado)
5. UDev Hook para suminsitrar imagen al conectar la rpi a una televisión
6. DRM Content (Selenium? webdriver, DRM content cant be piped to vlc, must be played from browser)

Todo es programación y configuración de la raspberry, nada es alambrado

## Consola de videojuegos retro

1. Custom boot logo
2. control usando gamepad o joystick (no teclado, mous)
3. 15 ROMs (juegos)

ROMS de NES, SNES y GameBoy Advance, no puedes usar Retropie, Recallbox, Batocera, Lakka, Pi Entertainment System, Skraper, entonces como cargas la ROM?

REQUIERE: un emulador esas consolas y configuración del joystick o gamepad, posiblemente conectado por USB a la raspberrypi

## Control de invernadero

Monitoreo y administración remota de un invernadero

1. Encendido y apagado de sistema de irrigación.
2. Desplegado de gráfica con historico de temperatura, irrigación y acciones tomadas.
3. Control de temperatura del invernadero utilizando PID.
4. Control de potencia del radiador (foco incandecente).
5. Control de potencia de ventilador.
6. Programado de ciclos de temperatura e irrigado.
7. Servidor web para control.

2 sensores de temperatura 
foco enciende cuando la temperatura es baja
ventilador lo contrario, bruh
sistema de irrigación: bomba de agua de baja potencia

Graficas con el historial de temperaturas y acciones tomadas.

¿ PID ?

## Concentrador básico - Smart Home

1. Desṕlegado de camaras de vigilancia (fakes, no requiere camaras reales)
2. Encedido y apago de luces (1 al mneos)
3. Atenuado de luces (1 al menos, modular potencia suministrada)
4. Detección de timbre de puerta (al menos uno)
5. Apertura remota de la puerta de la cochera
6. Programa de encendido y apagado de luces e interruptores (desde codigo)
7. Servidor web

Maqueta de casa, conectada a AC, usar openHAB or Home Assistan para control de focos, timbre y camaras

OpenHAB --> Permite controlar focos, timbres, camaras, motores?, que son compatibles con openHAB

OpenHABian SO ?

Push buttons, LED's, servomotores y componentes de DC no son aceptable.

## Distro de propósito especifico

