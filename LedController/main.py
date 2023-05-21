"""
LED Controller

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


def led_control_server():
    """
    Creates a simple HTTP server for controlling the on-board LED.
    """
    # Listen for connections on port 80 (HTTP Server Port)
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    sock = socket.socket()
    sock.bind(addr)
    sock.listen()

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

            # Check if client has requested an LED change
            request_url = request.split()[1]
            if request_url.find("/ledon") != -1:
                # Turn LED on
                led_state = True
                led.on()
            elif request_url.find("/ledoff") != -1:
                # Turn LED off
                led_state = False
                led.off()
            else:
                # Client has not requested a change
                pass

            # Get HTML page
            file = open("index.html")  # TODO: Fix html buttons for iOS
            html = file.read()
            file.close()

            # Now send HTML back to client with current LED state.
            html = html.replace("**ledState**", "ON" if led_state else "OFF")
            cl.send(html)
            cl.close()
        except OSError as e:
            # Client loses connection to server.
            cl.close()
            print('Connection Closed')


def main():
    """
    Main Loop
    """
    create_access_point(DEFAULT_WIFI["ssid"], DEFAULT_WIFI["pwd"])
    led_control_server()


if __name__ == '__main__':
    main()
