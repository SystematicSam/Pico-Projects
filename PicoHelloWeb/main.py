"""
Pico Hello Web

This module
"""
import time

import network

__author__ = "Sam Rogers"
__version__ = 0.1

DEFAULT_WIFI = {
    "ssid": "systematic",
    "pwd": "sam"
}


def create_network(ssid, pwd):
    # Configure device to act as a Wi-Fi access point
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=pwd)
    ap.active(True)

    # Wait for access point to go active
    wait_time = 0
    while not ap.active():
        print("Waiting for activation...", wait_time)
        wait_time += 1
        time.sleep(1)

    # Access point is now available
    status = ap.ifconfig()
    print("Wi-Fi Connected!")
    print("  IP Address:\t", status[0])
    print("  Subnet Mask:\t", status[1])
    print("  Gateway:\t", status[2])
    print("  DNS Server:\t", status[3])


def main():
    """
    Main Loop
    """
    create_network(DEFAULT_WIFI["ssid"], DEFAULT_WIFI["pwd"])


if __name__ == '__main__':
    main()
