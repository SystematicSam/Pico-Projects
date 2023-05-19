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
import ujson

__author__ = "Sam Rogers"
__version__ = "0.1"

DEFAULT_WIFI = {
    "ssid": "hello",
    "pwd": "world"
}


class WiFi:
    def __init__(self, cfg: dict):
        self.ssid = cfg.get("ssid", DEFAULT_WIFI["ssid"])
        self.pwd = cfg.get("pwd", DEFAULT_WIFI["pwd"])

        print("SSID:\t" + self.ssid)
        print("PWD:\t" + self.pwd)


def get_config(path: str) -> dict:
    with open(path, "r") as f:
        cfg = ujson.load(f)
        return cfg


def main(cfg: dict):
    wifi = WiFi(cfg.get("wifi"))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        main(get_config("config.json"))
    except OSError:
        print("Error opening config file! Exiting...")
        sys.exit(-1)
