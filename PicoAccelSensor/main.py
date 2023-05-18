"""
PiicoDev LIS3DH 3-Axis Accelerometer Sensor Program

This program reads linear and tilt angles from the PiicoDev
Accelerometer Sensor and outputs to PiicoDev OLED Display Module.
Tapping and shaking detection is also available.

Author: Sam Rogers

Created: 18/05/2023
"""
from PiicoDev_LIS3DH import PiicoDev_LIS3DH
from PiicoDev_Unified import sleep_ms
from console import Console

__author__ = "Sam Rogers"
__version__ = "0.2"


def main():
    """
    Main Loop

    Retrieves linear acceleration readings from sensor and prints to
    console display.
    """
    # Print startup message:
    display.println("Starting measurements:")
    display.refresh()
    for i in range(4):
        sleep_ms(100)
        display.println("   .")
        display.refresh()
    # Change line positions to make first line appear as a heading
    display.line_pos = [0, 15, 27, 39, 51]
    while True:
        x, y, z = sensor.acceleration  # linear accelerations
        # x, y, z = sensor.angle  # angles
        display.data[0] = "-Accelerometer-"
        display.data[1] = "  X: %.2f" % x
        display.data[2] = "  Y: %.2f" % y
        display.data[3] = "  Z: %.2f" % z
        if sensor.tapped:
            display.data[4] = "--TAPPED--"
        elif sensor.shake():
            display.data[4] = "--SHAKEN--"
        else:
            display.data[4] = ""

        display.refresh()
        sleep_ms(100)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sensor = PiicoDev_LIS3DH()
    sensor.range = 2
    display = Console()
    main()
