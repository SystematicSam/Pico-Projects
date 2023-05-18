"""
Pico Wi-Fi

This Micropython script acts as either an autonomous program or a
project attachable script to connect a Pico W device to the internet.

Main functionality is reading in a Wi-Fi configuration from config file
and then attempting a connection based on that configuration.  Errors
connecting are detected and appropriate messages displayed to user.

This script is most useful for testing a connection (autonomous) or
establishing a connection for data transfer later (project attachable).

Author: Sam Rogers

Created: 18/05/2023
"""
import json

__author__ = "Sam Rogers"
__version__ = "0.1"


def main():
    for param in config['secrets']:
        print(param)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    f = open("config.json", "r")
    config = json.load(f)
    main()
