"""
First Application

This Micropython script blinks the LED onboard the Pico and prints a
random multiple of 13 to the console every half a second.

Author: Sam Rogers

Created: 30/01/2023
"""
from machine import Pin
from time import sleep

__author__ = "Sam Rogers"
__version__ = "1.0"


def main():
    """
    Main Loop
    """
    # On-board LED has Pin name 'LED'
    led = Pin('LED', Pin.OUT)
    n = 0
    while True:
        # Toggles LED on/off
        led.toggle()
        print("13 times {} is {}".format(n, 13 * n))
        n += 1
        sleep(0.5)


if __name__ == '__main__':
    main()
