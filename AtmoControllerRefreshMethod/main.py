"""
PiicoDev BME280 Atmospheric Sensor Controller
"""
import network
import socket
import time
import ujson

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


def atmo_control_server():
    """
    Creates a simple HTTP server for controlling the on-board LED.
    """
    # Listen for connections on port 80 (HTTP Server Port)
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(addr)
    sock.listen(1)
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
        except OSError as e:
            # Client loses connection to server.
            print('Connection Closed')
        finally:
            cl.close()


def main():
    """
    Main Loop:
    """
    with open("config.json", "r") as f:
        cfg = ujson.load(f)
    connect_to_wifi(cfg.get("ssid", DEFAULT_WIFI["ssid"]),
                    cfg.get("pwd", DEFAULT_WIFI["pwd"]))
    atmo_control_server()


if __name__ == '__main__':
    main()
