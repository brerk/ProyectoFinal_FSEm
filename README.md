# ProyectoFinal_FSEm - Monitoreo y administración remota de un invernadero

TODO: 

1. Encendido y apagado de sistema de irrigación.
2. Desplegado de gráfica con historico de temperatura, irrigación y acciones tomadas.
3. Control de temperatura del invernadero utilizando PID.
X 4. Control de potencia del radiador (foco incandecente).
X 5. Control de potencia de ventilador. X
6. Programado de ciclos de temperatura e irrigado.
X 7. Servidor web para control.

Raspberry PI Os instalation

buildroot iso

2 sensores de temperatura 
foco enciende cuando la temperatura es baja
ventilador lo contrario, bruh
sistema de irrigación: bomba de agua de baja potencia

Graficas con el historial de temperaturas y acciones tomadas.

¿ PID ?

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


# Install

## Dependencies

    python pip virtualenv 

## Commands to clone and install python dependencies

    git clone https://github.com/brerk/ProyectoFinal_FSEm.git
    cd ProyectoFinal_FSem
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

    fastapi run server.py

In a browser open: `localhost:8000`
