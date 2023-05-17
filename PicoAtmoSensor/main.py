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

__author__ = "Sam Rogers"
__version__ = "0.1"


def main():
    while True:
        # Print data
        tempC, presPa, humRH = sensor.values()
        print(str(tempC) + " °C  " + str(presPa) + " hPa  " +
              str(humRH) + "%RH")

        # Altitude demo
        print(sensor.altitude() - zeroAlt)
        sleep_ms(100)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sensor = PiicoDev_BME280()  # initialise the sensor
    zeroAlt = sensor.altitude()  # take an initial altitude reading
    main()
