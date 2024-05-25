# I2C module to interact with Arduino One which acts as slave.
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
import struct
from typing import Union
import smbus2
from loguru import logger

SLAVE_ADDR = 0x0A  # I2C Address of Arduino One

i2c = smbus2.SMBus(1)


def read_temp_from_i2c(sensor_id: int) -> Union[float, None]:
    """
    Request from I2C the selected sensor_id (0, 1) and wait for a reply wich contains the temperature at that moment.
    """
    try:
        data = struct.pack("<B", sensor_id)
        msg = smbus2.i2c_msg.write(SLAVE_ADDR, data)
        i2c.i2c_rdwr(msg)  # Performs write

        msg = smbus2.i2c_msg.read(SLAVE_ADDR, 4)
        i2c.i2c_rdwr(msg)  # Performs write

        # Data decoding
        data = list(msg)  # Converts stream to list
        ba = bytearray()
        for c in data:
            ba.append(int(c))

        temp = struct.unpack("<f", ba)[0]

        return temp
    except Exception as ex:
        logger.warning(f"An error ocurred while reading from i2c slave: {ex}")
        return None


def send_cmd(device, value) -> None:
    """
    Send a change of value for light, fan or pump.

    The actual change is made by the arduino one.
    """
    devices_id = {"light": 0, "fan": 1, "pump": 2}

    device_id = devices_id.get(device, None)

    if not device_id:
        print(f"Devide: {device} is not valid.")
        return

    try:
        data = struct.pack("<Bf", device_id, value)
        msg = smbus2.i2c_msg.write(SLAVE_ADDR, data)
        i2c.i2c_rdwr(msg)  # Performs write
    except Exception as ex:
        print(f"An error ocurred while sending data to arduino one: {ex}")
