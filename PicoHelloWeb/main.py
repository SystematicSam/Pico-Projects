"""
Pico Hello Web

A python script for setting up a Raspberry Pi Pico W as an access point
for a simple http server.  The server returns a simple greeting for
each client connection.

Author: Sam Rogers

Created: 21/05/2023

Requires: Raspberry Pi Pico W with Micropython
"""
import network
import socket
import time
from machine import Pin

__author__ = "Sam Rogers"
__version__ = 0.1

# Default parameters for the Wi-Fi access point
DEFAULT_WIFI = {
    "ssid": "Systematic",
    "pwd": "systemic"
}

# Basic HTML Page
HTML = """<!DOCTYPE html>
<html>
    <head> <title>Pico W</title> </head>
    <body> <h1>Pico W says Hello</h1>
        <p>Greetings to the World Wide Web.</p>
    </body>
</html>
"""


def create_access_point(ssid, pwd):
    """
    Create a visible access point, using the given ssid and password,
    for other devices to connect to.

    :param ssid: the ssid of the access point
    :param pwd: the password to connect to the access point
    """
    # Configure device to act as a Wi-Fi access point
    ap = network.WLAN(network.AP_IF)
    ap.active(False)
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
    print("Wi-Fi Active!")
    print("  IP Address:\t", status[0])
    print("  Subnet Mask:\t", status[1])
    print("  Gateway:\t", status[2])
    print("  DNS Server:\t", status[3])


def http_server():
    """
    Creates a simple HTTP server.
    """
    # Listen for connections on port 80 (HTTP Server Port)
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    sock = socket.socket()
    sock.bind(addr)
    sock.listen(1)

    # Using on-board LED to indicate connection status
    led = Pin("LED", Pin.OUT)
    led.off()

    # Listen for connections, respond to client requests
    while True:
        try:
            # Accept client connections and print requests to console.
            cl, addr = sock.accept()
            print("Client connected from: ", addr)
            request = cl.recv(1024)
            led.on()
            print(request.decode("utf-8"))

            # Respond to clients with simple HTML page to be displayed.
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(HTML)
            cl.close()
            led.off()
        except OSError as e:
            # Client loses connection to server.
            cl.close()
            print('Connection Closed')


def main():
    """
    Main Loop

    Configures the Raspberry Pi Pico W as an access point and setups a
    simple HTTP server to respond to connections.
    """
    create_access_point(DEFAULT_WIFI["ssid"], DEFAULT_WIFI["pwd"])
    http_server()


if __name__ == '__main__':
    main()
