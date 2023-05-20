"""
This module connects provides functionality for connecting a Micropython
device (usually a Raspberry Pi Pico W) to an existing Wi-Fi network.

Author: Sam Rogers

Created: 18/05/2023

Requires: Micropython Capable Device
"""

import sys
import time

import ujson
import network

__author__ = "Sam Rogers"
__version__ = "0.2"

# Default values if Wi-Fi configuration not specified
DEFAULT_WIFI = {
    "ssid": "hello",
    "pwd": "world"
}


def connect_to_wifi(ssid: str, pwd: str):
    """
    Connect to an existing Wi-Fi network.

    :param ssid: the name of the network to connect to
    :param pwd: the password to connect to the network
    """
    # Setup Pico in station mode and attempt Wi-Fi connection
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, pwd)

    # Wait for connection
    timeout = 0
    while timeout < 10:
        """
        # wlan.status() return values and meanings:
            0  STAT_LINK_DOWN       -> Link is down
            1  STAT_LINK_JOIN       -> Connecting to wifi
            2  STAT_LINK_NOIP       -> Connected to wifi, no ip
            3  STAT_LINK_UP         -> Connected to wifi, got ip
            -1 STAT_LINK_FAIL       -> Connection attempted, but failed
            -2 STAT_LINK_NONET      -> No network found with ssid
            -3 STAT_LINK_BADAUTH    -> Bad authentication (wrong password)
        """
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        timeout += 1
        print("Waiting for connection...", timeout)
        time.sleep(1)

    # Handle connection status
    if wlan.status() != 3:
        # Connection failed for some reason
        raise RuntimeError("Wi-Fi Connection Failed!\nError Code:" + str(wlan.status()))
    else:
        # Connection successful
        status = wlan.ifconfig()
        print("Wi-Fi Connected!")
        print("  IP Address:\t", status[0])
        print("  Subnet Mask:\t", status[1])
        print("  Gateway:\t", status[2])
        print("  DNS Server:\t", status[3])


def get_config(path: str) -> dict:
    """
    Gets the configuration parameters as a dictionary.

    :param path: the path to the config file
    :return: the config dictionary
    """
    with open(path, "r") as f:
        cfg = ujson.load(f)
        return cfg


def main():
    """
    Main Loop

    Get Wi-Fi configuration from config file, or default configuration
    if no config file provided, and connect to the specified network.
    """
    try:
        with open("config.json", "r") as f:
            cfg: dict = ujson.load(f)
    except OSError:
        print("Error opening config file! Exiting...")
        sys.exit(-1)
    connect_to_wifi(cfg.get("ssid", DEFAULT_WIFI["ssid"]),
                    cfg.get("pwd", DEFAULT_WIFI["pwd"]))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
