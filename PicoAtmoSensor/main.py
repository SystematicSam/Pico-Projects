"""
PiicoDev BME280 Atmospheric Sensor Program

This program reads Temperature, Pressure and Relative Humidity
from the PiicoDev Atmospheric Sensor and outputs to PiicoDev OLED
Display Module. An altitude reading is also available.

Author: Sam Rogers

Created: 17/05/2023
"""
from PiicoDev_BME280 import PiicoDev_BME280
from PiicoDev_Unified import sleep_ms
from console import Console

__author__ = "Sam Rogers"
__version__ = "0.1"


def main():
    """
    Main Loop

    Retrieves temperature, humidity, pressure and altitude readings
    from sensor and prints to console display.
    """
    # Print startup message:
    display.println("Starting measurements:")
    display.refresh()
    for i in range(4):
        sleep_ms(100)
        display.println("   .")
        display.refresh()
    display.line_pos = [0, 15, 27, 39, 51]
    while True:
        # Retrieve data
        tempC, presPa, humRH = sensor.values()
        heading = "---Atmo Sensor---"
        temp = "TMP: " + str(tempC) + chr(176) + "C"
        pres = "PRE: " + str(presPa / 100) + "hPa"
        hum = "HUM: " + str(round(humRH, 2)) + "%RH"
        alt = "ALT: " + str(round(sensor.altitude() - zero, 2)) + "m"

        # Display data
        display.data = [heading, temp, pres, hum, alt]
        display.refresh()

        # 100 millisecond intervals
        sleep_ms(100)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sensor = PiicoDev_BME280()  # initialise the sensor
    zero = sensor.altitude()  # take an initial altitude reading
    display = Console() # initalise OLED module for console printing
    main()
