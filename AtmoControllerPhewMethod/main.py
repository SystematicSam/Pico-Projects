"""
PiicoDev BME280 Atmospheric Sensor Controller
"""
import network
import socket
import time
import ujson
from PiicoDev_BME280 import PiicoDev_BME280

__author__ = "Sam Rogers"
__version__ = "0.1"

# Default Wi-Fi network parameters
DEFAULT_WIFI = {
    "ssid": "Samuel\u2019s iPhone",
    "pwd": "1qaz7ujm",
}


def connect_to_wifi(ssid, pwd):
    """
    Connect to an existing Wi-Fi, using the given ssid and password.

    :param ssid: the ssid of the Wi-Fi network
    :param pwd: the password to connect to the network
    """
    # Setup Pico in station mode and attempt Wi-Fi connection
    print(ssid, pwd)
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
        raise RuntimeError(
            "Wi-Fi Connection Failed!\nError Code:" + str(wlan.status()))
    else:
        # Connection successful
        status = wlan.ifconfig()
        print("Wi-Fi Connected!")
        print("  IP Address:\t", status[0])
        print("  Subnet Mask:\t", status[1])
        print("  Gateway:\t", status[2])
        print("  DNS Server:\t", status[3])


def main():
    """
    Main Loop
    """
    pass


if __name__ == '__main__':
    main()
