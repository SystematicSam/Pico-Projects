"""
LED Controller Interface

This module creates a simple HTTP server on the Raspberry Pi Pico W so
that a user can control the on-board LED from a webpage.

Author: Sam Rogers

Created: 22/05/2023

Requires: Raspberry Pi Pico W with Micropython
"""
import network
import socket
import time
from machine import Pin

__author__ = "Sam Rogers"
__version__ = "1.0"

# Default parameters for the Wi-Fi access point
AP = {
    "ssid": "Systematic",
    "pwd": "systemic"
}


def create_access_point(ssid, pwd):
    """
    Create a visible access point, using the given ssid and password,
    for other devices to connect to.

    :param ssid: the ssid of the access point
    :param pwd: the password to connect to the access point
    """
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
    print("Wi-Fi Active!")
    print("  IP Address:\t", status[0])
    print("  Subnet Mask:\t", status[1])
    print("  Gateway:\t", status[2])
    print("  DNS Server:\t", status[3])


def led_control_server():
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

    # LED starts in OFF state
    led = Pin("LED", Pin.OUT)
    led.off()
    led_state = False

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
            if request_url == "/ledon":
                # User turns LED on
                led_state = True
                led.on()
                cl.send("The LED is ON")
            elif request_url == "/ledoff":
                # User turns LED off
                led_state = False
                led.off()
                cl.send("The LED is OFF")
            elif request_url == "/favicon.ico":
                # Returns image requests for browser tab icon
                cl.send("HTTP/1.1 200 OK\r\nContent-type: image/png\r\n\r\n")
                with open("led.png", "rb") as file:
                    while True:
                        data = file.read(1024)
                        if not data:
                            break;
                        cl.sendall(data)
            else:
                # Homepage
                with open("index.html") as file:
                    html = file.read()
                html = html.replace("**ledState**",
                                    "ON" if led_state else "OFF")
                cl.send(html)
            cl.close()
        except OSError as e:
            # Client loses connection to server.
            cl.close()
            print('Connection Closed')


def main():
    create_access_point(AP["ssid"], AP["pwd"])
    led_control_server()


if __name__ == '__main__':
    main()
