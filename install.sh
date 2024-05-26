#!/bin/bash

# Install Script: Prepares the rasbpberry and install the smart greenhouse.
# Copyright (C) 2024  Erik Bravo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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

echo "Firewall configuration..."
ufw allow ssh
ufw allow 8000 comment "invernadero web interface"
ufw enable

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

echo "Smart Greenhouse installed, it will be available on the next system startup on http://localhost:8000"
echo "Now, restar the system with 'reboot'"


