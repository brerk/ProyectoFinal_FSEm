#!/bin/bash

if [ "$EUID" -ne 0 ]
then echo "Script must be run as root. (try sudo su?)"
  exit
fi

echo "Enable 1-Wire"
echo "dtoverlay=w1-gpio" >> /boot/firmware/config.txt

echo "Eable I2C mod"
raspi-config nonint do_i2c 0

echo "Installing system dependencies"
apt-get install i2c-tools python3-smbus2 python3-pip virtualenv ufw git python3-rpi.gpio -y
adduser pi i2c

modprobe w1-gpio
modprobe w1-therm

echo "Connected 1-wire devices."
ls sys/bus/w1/devices

ufw allow 8000 comment "invernadero web interface"

echo "Proyect Installation..."


cd /home/pi
git clone https://github.com/brerk/ProyectoFinal_FSEm.git
chown -R pi:pi /home/pi/ProyectoFinal_FSEm
cd ProyectoFinal_FSEm

echo "Creating Virtual environment..."
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

echo "Installing proyect as service..."

cat << EOF > /etc/systemd/system/invernadero.service
[Unit]
Description=Invernadero Inteligente 
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/ProyectoFinal_FSEm
Environment=PYTHONPATH=/home/pi/ProyectoFinal_FSEm/venv
ExecStart=/home/pi/ProyectoFinal_FSEm/venv/bin/fastapi run server.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now inveradero.service
