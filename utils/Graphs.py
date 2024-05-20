import matplotlib.pyplot as plt

# import numpy as np


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

    # print(f"{len(temps_prom_x)=} {len(temps_prom_y)=}")
    # print(f"{len(s0_x)=} {len(s0_y)=}")
    # print(f"{len(s1_x)=} {len(s1_y)=}")

    fig, ax = plt.subplots()

    ax.plot(temps_prom_x, temps_prom_y, marker="*", linewidth=1.0, label="Prom")
    ax.plot(s0_x, s0_y, linewidth=1.0, label="S0", marker="*")
    ax.plot(s1_x, s1_y, linewidth=1.0, label="S1", marker="*")

    plt.title("Time vs Temperature Measurement")
    plt.xlabel("HH:MM:SS")
    plt.ylabel("°Celsius")

    plt.grid()
    plt.legend()

    plt.savefig("./static/temps.jpg")
