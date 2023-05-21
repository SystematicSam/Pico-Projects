"""
Pico Hello Web

This module
"""
import network
import socket
import time
from machine import Pin

__author__ = "Sam Rogers"
__version__ = 0.1

DEFAULT_WIFI = {
    "ssid": "Systematic",
    "pwd": "systemic"
}

HTML = """<!DOCTYPE html>
<html>
    <head> <title>Pico W</title> </head>
    <body> <h1>Pico W</h1>
        <p>Hello from Pico W.</p>
    </body>
</html>
"""


def create_network(ssid, pwd):
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
            cl, addr = sock.accept()
            print("Client connected from: ", addr)
            request = cl.recv(1024)
            led.on()
            print(request.decode("utf-8"))

            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(HTML)
            cl.close()
            led.off()
        except OSError as e:
            cl.close()
            print('Connection Closed')




def main():
    """
    Main Loop
    """
    create_network(DEFAULT_WIFI["ssid"], DEFAULT_WIFI["pwd"])
    http_server()

if __name__ == '__main__':
    main()
