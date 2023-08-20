import os
import wifi, ipaddress, socketpool
from time import sleep
from binascii import hexlify

pool = socketpool.SocketPool(wifi.radio)
ping_target = ipaddress.ip_address('8.8.8.8')

def connect_to_wifi():
    for i in range(5):
        try:
            wifi.radio.hostname = 'Fun-Clock'
            wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASS"))
            print(f'connected to wifi {os.getenv("WIFI_SSID")}')
            break
        except ConnectionError as e:
            print(f'cannot connect to wifi: {e}')
            sleep(1)


def get_socket_pool():
    ping = wifi.radio.ping(ping_target, timeout=1)
    semicolon = ':'
    print(f'network status: name {wifi.radio.hostname}, ip {wifi.radio.ipv4_address}, mac {hexlify(wifi.radio.mac_address, semicolon)}, ping {ping} seconds')
    return pool


if __name__ == '__main__':
    connect_to_wifi()
    get_socket_pool()