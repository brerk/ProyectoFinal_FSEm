import smbus2, struct
from time import sleep

from loguru import logger

# Arduino's I2C device address
SLAVE_ADDR = 0x0A # I2C Address of Arduino 1

# Initialize the I2C bus;
# RPI version 1 requires smbus.SMBus(0)
i2c = smbus2.SMBus(1)

class LightControl:
    def writePower(pwr):
        try:
            data = struct.pack('<f', pwr) # Packs number as float
            msg = smbus2.i2c_msg.write(SLAVE_ADDR, data)
            i2c.i2c_rdwr(msg)  # Performs write
        except:
            logger.warning("An error ocurred while writing to SLAVE_ADDR")

lc = LightControl()
