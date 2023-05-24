"""
PiicoDev BME280 Atmospheric Sensor Controller

This module creates a simple HTTP server on a Raspberry Pi Pico W so
that a user can control an attached PiicoDev BME280 Atmospheric Sensor
from a webpage.  Also, data is updated in half second intervals on
the webpage with new values.

NOTE: Best browser access is from Firefox (no stuttering)

Author: Sam Rogers

Created 24/05/2023

Requires: Raspberry Pi Pico W with Micropython
"""
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

# Initialise sensor
atmo = PiicoDev_BME280()
zero = atmo.altitude()


@server.route("/temp")
def temperature(request):
    """
    Get the current temperature from the BME280.

    :param request: an object representation of the HTTP request
    :return: a message with the current temperature in degrees Celsius
    """
    return "TEMP: %.2f\xb0C" % atmo.values()[0]


@server.route("/press")
def pressure(request):
    """
    Get the current atmospheric pressure from the BME280.

    :param request: an object representation of the HTTP request
    :return: a message with the current pressure in hectopascals
    """
    return "PRESS: %.2fhPa" % (atmo.values()[1] / 100)


@server.route("/humid")
def relative_humidity(request):
    """
    Get the current relative humidity from the BME280.

    :param request: an object representation of the HTTP request
    :return: a message with the current relative humidity
    """
    return "HUM: %.2f%%RH" % atmo.values()[2]


@server.route("/alt")
def altitude(request):
    """
    Get the current altitude of BME280 relative to initial altitude.

    :param request: an object representation of the HTTP request
    :return: a message with the current altitude
    """
    return "ALT: %.2fm" % (atmo.altitude() - zero)


@server.route("/favicon.ico")
def favicon(request):
    """
    Get the image to be used as the favicon in a browser webpage.

    :param request: an object representation of the HTTP request
    :return: the favicon image
    """
    with open("icon.png", "rb") as f:
        body = b''
        while True:
            data = f.read(1024)
            if not data:
                break
            body += data
        return server.Response(body, headers={"Content-Type": "image/png"})


@server.catchall()
def catchall(request):
    """
    Catch all non-handled client requests and respond with the default
    webpage (index.html).

    :param request: an object representation of the HTTP request
    :return: the default webpage html
    """
    return render_template("index.html")


def main():
    """
    Main Loop

    Load Wi-Fi configuration from config file, connect to specified
    network and start micropython-phew HTTP server.
    """
    with open("config.json", "r") as f:
        cfg = ujson.load(f)
    wifi = connect_to_wifi(cfg.get("ssid", DEFAULT_WIFI["ssid"]),
                           cfg.get("pwd", DEFAULT_WIFI["pwd"]))
    print("Wi-Fi Connected!\nIP: " + wifi)
    server.run()


if __name__ == '__main__':
    main()
