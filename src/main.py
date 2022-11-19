#!/usr/bin/env python

import time
import math
import binascii
import ustruct
import pycom
from pycoproc_2 import Pycoproc
import machine
import socket
from network import LoRa
from SI7006A20 import SI7006A20

sleep_time_s = 60*15 # Set sleep time to 15 minutes

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

dev_eui = binascii.unhexlify('ADD_DEV_EUI')
app_eui = binascii.unhexlify('ADD_APP_EUI')
app_key = binascii.unhexlify('ADD_APP_KEY')

lora.nvram_restore()
if(lora.has_joined() == False):
    print("Not joined yet...")
    lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)
else:
    print("Joined!")

while not lora.has_joined():
    time.sleep(2.5)
    print('Not joined yet...')

print('Network joined!')

print("Sleep 1 second...")
time.sleep(1) # sleep to be able to interupt

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

pycom.heartbeat(False) # heartbeat until connected
pycom.rgbled(0x000505) # green light while sending sensor data

py = Pycoproc()
py.setup_sleep(sleep_time_s)

while True:
    si = SI7006A20(py)
    temperature = float(round(si.temperature(),1))
    humidity = float(round(si.humidity(),1))
    # set your battery voltage limits here
    # probneed to look in to this battery part, took it from a Pycom script
    vmax = 4.2
    vmin = 3.3
    battery_voltage = float(round(py.read_battery_voltage(),1))
    battery_percentage = float(round(((battery_voltage - vmin / (vmax - vmin))*100),1))

    s.setblocking(True)
    s.send(ustruct.pack('<4f', temperature, humidity, battery_voltage, battery_percentage))
    s.setblocking(False)

    print('sent temperature:', temperature)
    print('sent humidity:', humidity)
    print("Battery voltage: " + str(py.read_battery_voltage()), " percentage: ", battery_percentage)
    lora.nvram_save()
    print("Time to deep sleep...")
    py.go_to_sleep(False)
