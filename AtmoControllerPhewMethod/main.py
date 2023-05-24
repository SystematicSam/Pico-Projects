"""
PiicoDev BME280 Atmospheric Sensor Controller
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


@server.route("/favicon.ico")
def favicon(request):
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
    return render_template("index.html")


def main():
    """
    Main Loop
    """
    with open("config.json", "r") as f:
        cfg = ujson.load(f)
    wifi = connect_to_wifi(cfg.get("ssid", DEFAULT_WIFI["ssid"]),
                    cfg.get("pwd", DEFAULT_WIFI["pwd"]))
    print("Wi-Fi Connected!\nIP: " + wifi)
    server.run()


if __name__ == '__main__':
    main()
