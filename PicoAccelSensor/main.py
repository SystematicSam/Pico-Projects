"""
PiicoDev LIS3DH 3-Axis Accelerometer Sensor Program

This program reads linear and angular accelerations from the PiicoDev
Accelerometer Sensor and outputs to PiicoDev OLED Display Module.
Tapping and shaking detection is also available.

Author: Sam Rogers

Created: 18/05/2023
"""
from PiicoDev_LIS3DH import PiicoDev_LIS3DH
from PiicoDev_Unified import sleep_ms
from console import Console

__author__ = "Sam Rogers"
__version__ = "0.1"


def main():
    """
    Main Loop


    """
    while True:
        x, y, z = sensor.acceleration
        x = round(x, 2)
        y = round(y, 2)
        z = round(z, 2)
        readout = "X: " + str(x) + ", Y: " + str(y) + ", Z: " + str(z)
        print(readout)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sensor = PiicoDev_LIS3DH()
    sensor.range = 2
    main()