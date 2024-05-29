# ProyectoFinal_FSEm - Proyecto Final - Invernadero Inteligente


## Material
- Socket para foco
- Foco (no ahorrado, revisar p7)
- Sensor DSXXXXXX
- Cable Calibre 22 AWG
- Pecera
- Ventilador
- Jumpers
- Diodos, resistencias, cable para AC
- Bomba de agua para acuario y manguera para agua.
- Clavija
- Protoboard
- Raspberry Pi 3B+ o Superior


# Dependencies

- python
- apscheduler
- ufw
- fastapi
- SQLAlchemy
- APScheduler
- loguru
- smbus2

# Install instructions

Se asume que el usuario **ya cuenta con Raspberry Pi OS Lite** instalado en una Memoria MicroSD de al menos 8Gb Clase 10 y
que este cuenta con acceso a una sesión en la raspberry como usuario root (se sugiere utilizar SSH).

Para instalar este proyecto se cuenta con un script que realiza toda la configuración necesaria de la raspberry pi 4.
Este descarga el proyecto directamente desde este repositorio, instalas las dependencias a nivel del sistema, crea un
entorno virtual para ejecutar el invernadero, crea un servicio de systemd e inicializa el proyecto para empezar a servir
la interfaz web del servidor en el puerto 8000.

Para instalar y configurar las dependencias:

    sudo su
    cd /home/pi
    wget https://raw.githubusercontent.com/brerk/ProyectoFinal_FSEm/main/install.sh
    chmod +x install.sh
    ./install.sh

Reiniciar las raspberry pi:

    reboot

Para acceder a la interfaz web basta con entrar en 🌐 `localhost:8000`. El servidor escucha tambien en la interfaz wlan0, por lo que esta interfaz tambien es accessible desde otros dispositivos conectados a la misma red.
