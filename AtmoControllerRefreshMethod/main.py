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


def atmo_control_server(atmo: PiicoDev_BME280, zero: float):
    """
    Creates a simple HTTP server for controlling the on-board LED.
    """
    # Listen for connections on port 80 (HTTP Server Port)
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(addr)
    sock.listen()
    print("Listening....")

    # Listen for connections, respond to client requests
    while True:
        try:
            # Accept client connections and print requests to console.
            cl, addr = sock.accept()
            print("Client connected from: ", addr)
            request = cl.recv(1024).decode("utf-8")
            print(request)

            # Request processing
            request_url = request.split()[1]
            if request_url == "/temp":
                # TODO: Return temperature data
                pass
            elif request_url == "/press":
                # TODO: Return pressure data
                pass
            elif request_url == "/humid":
                # TODO: Return humidity data
                pass
            elif request_url == "/alti":
                # TODO: Return altitude data
                pass
            elif request_url == "/favicon.ico":
                cl.send("HTTP/1.1 200 OK\r\nContent-type: image/png\r\n\r\n")
                with open("icon.png", "rb") as f:
                    while True:
                        data = f.read(1024)
                        if not data:
                            break
                        cl.sendall(data)
            else:
                with open("index.html") as f:
                    html = f.read()
                    html = html.replace("**READING**", "Please select an "
                                                       "option to begin")
                    cl.send(html)
            cl.close()
        except OSError as e:
            # Client loses connection to server.
            print('Connection Closed')



def main():
    """
    Main Loop:
    """
    with open("config.json", "r") as f:
        cfg = ujson.load(f)
    connect_to_wifi(cfg.get("ssid", DEFAULT_WIFI["ssid"]),
                    cfg.get("pwd", DEFAULT_WIFI["pwd"]))
    atmo = PiicoDev_BME280()  # Initialise sensor
    zero = atmo.altitude  # Zero Point for Attitude
    atmo_control_server(atmo, zero)


if __name__ == '__main__':
    main()
