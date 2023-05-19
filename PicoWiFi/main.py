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
import sys
import time

import ujson
import network

__author__ = "Sam Rogers"
__version__ = "0.1"

# Default values if Wi-Fi configuration not specified
DEFAULT_WIFI = {
    "ssid": "hello",
    "pwd": "world"
}


class WiFi:
    """
    A network connection, using Wi-Fi.

    :ivar ssid: the SSID of the network
    :ivar pwd: the password to connect to the network
    """
    def __init__(self, cfg: dict):
        """
        Initialises the Wi-Fi configuration.

        :param cfg: the config dictionary
        """
        self.ssid = cfg.get("ssid", DEFAULT_WIFI["ssid"])
        self.pwd = cfg.get("pwd", DEFAULT_WIFI["pwd"])
        print("SSID:\t" + self.ssid)
        print("PWD:\t" + self.pwd)

    def connect(self):
        """
        Connects to the Wi-Fi network, if possible.

        :raises RuntimeException: if connection fails or timeouts
        """
        # Setup Pico in station mode and attempt Wi-Fi connection
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.ssid, self.pwd)

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
            raise RuntimeError("Wi-Fi Connection Failed!\nError Code:",
                               wlan.status())
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


def main(cfg: dict):
    """
    Main Loop

    Creates WiFi object with configuration parameters and then connects
    to the specified network.

    :param cfg: the config dictionary
    """
    wifi = WiFi(cfg.get("wifi"))
    wifi.connect()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        main(get_config("config.json"))
    except OSError:
        print("Error opening config file! Exiting...")
        sys.exit(-1)
