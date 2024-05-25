# Graph: Creates a graph using previous temperature measurements.
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

import matplotlib.pyplot as plt


def create_temps_graph(
    s0_temps: list, s1_temps: list, output: str = "./static/temps.jpg"
):
    temps_prom_x = [s0_temp["timestamp"] for s0_temp in s0_temps]
    temps_prom_y = [
        (s0_temp["temp"] + s1_temp["temp"]) / 2
        for s0_temp, s1_temp in zip(s0_temps, s1_temps)
    ]

    s0_x = [row["timestamp"] for row in s0_temps]
    s0_y = [row["temp"] for row in s0_temps]

    s1_x = [row["timestamp"] for row in s1_temps]
    s1_y = [row["temp"] for row in s1_temps]

    fig, ax = plt.subplots()

    ax.plot(temps_prom_x, temps_prom_y, marker="*", linewidth=1.0, label="Prom")
    ax.plot(s0_x, s0_y, linewidth=1.0, label="S0", marker="*")
    ax.plot(s1_x, s1_y, linewidth=1.0, label="S1", marker="*")

    plt.title("Time vs Temperature Measurement")
    plt.xlabel("HH:MM:SS")
    plt.ylabel("°Celsius")

    plt.grid()
    plt.legend()

    plt.savefig(output)
