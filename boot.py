import os
import uos
from network import WLAN
from machine import UART
import machine
uart = UART(0, 115200)
os.dupterm(uart)

wlan=WLAN(mode=WLAN.STA)
def wlanConnect():
    nets = wlan.scan()
    for net in nets:
        if net.ssid == 'ParklifePiFi':
            print('Network found!')
            #credentials of temp Pi wifi: 'ParklifePiFi','lileedev'
            wlan.connect(net.ssid, auth=(net.sec, 'lileedev'), timeout=5000)
            while not wlan.isconnected():
                machine.idle() # save power while waiting
            print('WLAN connection succeeded!')
            break
