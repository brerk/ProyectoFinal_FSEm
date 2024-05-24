# import os
import glob
import time
from typing import Union

# These two lines mount the device:
# os.system("modprobe w1-gpio")
# os.system("modprobe w1-therm")

base_dir = "/sys/bus/w1/devices/"
device_folders = glob.glob(base_dir + "28*")


class TempSensor:
    def __init__(self, device_file: str) -> None:
        self.device_file = device_file

    def _read_temp_raw(self):
        f = open(self.device_file, "r")
        lines = f.readlines()
        f.close()

        return lines

    def read_temp(self) -> Union[float, None]:
        lines = self._read_temp_raw()

        while lines[0].strip()[-3:] != "YES":
            time.sleep(0.2)
            lines = self._read_temp_raw()

        temp_string = lines[-1].split("t=")[1]

        temp_c = float(temp_string) / 1000.0

        equals_pos = lines[1].find("t=")

        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2 :]

            temp_c = float(temp_string) / 1000.0

            return temp_c

        return None


# if __name__ == "__main__":
#     while True:
#         temp_c = read_temp()
#
#         if not temp_c:
#             print("Couldn't read temperature from file.")
#             continue
#
#         # print(f"Temperature --> C: {temp_c:3.3f}, F: {temp_f:3.3f}")
#         print(f"Temperature --> C: {temp_c:3.3f}")
#
#         time.sleep(1)

S0 = TempSensor(device_folders[0] + "/w1_slave")
S1 = TempSensor(device_folders[1] + "/w1_slave")


if __name__ == "__main__":
    while True:
        print(f"S0 --> {S0.read_temp()}, S1 --> {S1.read_temp()}")

        time.sleep(1)
