"""
PiicoDev BME280 Atmospheric Sensor Controller
"""
import network
import socket
import time
import ujson
from phew import server, connect_to_wifi
from phew.template import render_template
from PiicoDev_BME280 import PiicoDev_BME280


__author__ = "Sam Rogers"
__version__ = "0.1"

# Default Wi-Fi network parameters
DEFAULT_WIFI = {
    "ssid": "Samuel\u2019s iPhone",
    "pwd": "1qaz7ujm",
}



def main():
    """
    Main Loop
    """
    with open("config.json", "r") as f:
        cfg = ujson.load(f)
    connect_to_wifi(cfg.get("ssid", DEFAULT_WIFI["ssid"]),
                    cfg.get("pwd", DEFAULT_WIFI["pwd"]))
    atmo = PiicoDev_BME280()
    zero = atmo.altitude()


if __name__ == '__main__':
    main()
