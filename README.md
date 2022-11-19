# Sauna Monitor
###### tags: `LoRa` `IoT` `planning` `examination`
---
**Author**: Daniel Sixtensson

**Course**: Applied Internet of Things (Professional Education), 4DV119, Linneus University, 2022

**Table of Contents**

- [Project overview](#Project-overview)
- [Objectives](#Objectives)
- [Material](#Material)
- [Environment setup](#Environment-setup)
- [Putting everything together](#Putting-everything-together)
- [Platforms and infrastructure](#Platforms-and-infrastructure)
- [The code](#The-code)
- [The physical network layer](#The-physical-network-layer)
- [Visualisation and user interface](#Visualisation-and-user-interface)
- [Finalizing the design](#Finalizing-the-design)
- [Next step????](#Next-step)


### Project overview

The main goal was to learn something new and the goal with this project is to build an IoT device that can collect sensor data like temperature and humidity from the sauna and publish the data on a website.
With all material available and some basic knowledge in programming this project should probably not take more then a day to complete.


### Objectives

The initial project idea was to build a device to get the water temperature in the lake at the community sauna where I live and publish it on the booking website for the sauna. During the course I switched direction a bit an focused on the sauna instead. I thought it would be interesting to gather some data from when the sauna is being used and in the future use that data to do predictions on how long time it would take to heat up the sauna to a specific temperature depending on the start temperature and humidity. Therefore I decided on limiting this project to build a device to gather the data and publish the temperature on the sauna booking website as information to the people using the sauna.

With no previous knowledge about LoRa this was the most interesting part of the project to explore but the programming and playing with electronics was also really fun.

### Material

For this project you need a micro controller with LoRa support and sensors to gather the data. In my case I was able to use the sensors on the Pysenese 2.0 X board but if you use another setup you need to get sensors that can measure temperature and humidity. An alternative setup is not covered in this report. You will also need an antenna to be able to establish a connection to a LoRaWAN gateway. I you are not in reach of a gateway you need to get one and setup it up. This is not covered in this report. I was lucky that a neighbor had a gateway available that I was able to reach and connect to.


| Component | Description        |Price (SEK)| Supplier|
| --------- | ---------------- |||
| [FiPy](https://pycom.io/product/fipy/)   | ESP32 development board from Pycom |*|Pycom/Electrokit|
| [Pysense 2.0 X](https://pycom.io/product/pysense-2-0-x/)   | Shield from Pycom with onboard sensors |*|Pycom/Electrokit|
| [LoRa / Sigfox Antenna](https://pycom.io/product/lora-868mhz-915mhz-sigfox-antenna-kit/) | External antenna for LoRa/Sigfox |*| Pycom/Electrokit|
| [Li-Po battery](https://www.kjell.com/se/produkter/el-verktyg/arduino/arduino-tillbehor/luxorparts-li-po-batteri-37-v-med-kontakt-1200-mah-p87924) | Re-chargeable Li-Po battery to power the device |99,90| Kjell & Company|
| [Casing](https://www.biltema.se/bygg/elinstallationer/eldosor/kopplingsdosa-2000034324) | Casing to put the device in |36,90| Biltema|

[*] This item was part of a bundle from Electrokit created for a previous course at LNU. Total price for bundle was 1499 SEK and the complete list of included parts can be found on this [link](https://www.electrokit.com/produkt/lnu-1dt305-tillampad-iot-fipy-and-sensors-bundle/).

I choose the FiPy board from Pycom since it had many networks included in one board that ment that if I would not get one network to work in the sauna I would have the possibility to try another network.

![LoPy!](/img/material.jpg)
Fig. 1. Material list(images from Pycom, Biltema and Kjell & Company)


### Environment setup

Before getting into programming the FiPy there were some initial steps that I needed to perform. These steps included installing drivers for Windows and updating the firmware on both the Pysense 2.0 X and the FiPy. For these steps I followed a guide found [here](https://core-electronics.com.au/guides/pycom-pysense-pytrack-firmware-update/). It describes all the tools and files needed to perform this.

A guide on updating the firmware on the FiPy board can be found [here](https://docs.pycom.io/updatefirmware/device/).

When setting up the IDE i planned to use VS Code since I already had that installed but after having issues to get the connection to the FiPy I installed Atom instead and got it working. I spent some time on trying to get it to work with VS Code but after Atom was installed I stopped that.

Installing Atom and the Pymakr package that enables you to communicate with the FiPy board using the built in command line REPL was a simple task. Links to [Atom.io](https://atom.io/) and [Pymakr](https://atom.io/packages/pymakr). **Note** *Atom.io are archiving Atom and all projects under the Atom organization for an official sunset on December 15, 2022. Read more [here](https://github.blog/2022-06-08-sunsetting-atom/)*.

After connecting the board to the computer using a micro USB cable the status in Atom changes to Connected and you can now run MicroPython commands in the terminal directly on the board. After creating a MicroPython file you can either run it or upload/flash it to the bord and it will be run after the board has restarted.

In this project the amount of code was limited and I therefore only used the boot.py and main.py files to contain my code for the project. There are some libraries included in the project that are stored in a lib folder. The libraries are needed for using the onboard sensors on the Pysense board.

### Putting everything together

The assembly of this device was very simple since I did not use any external sensors but utilized the sensors built in on the Pysense 2.0 X board and therefore it was just to put the FiPy on the Pysense board and connect the antenna and the battery.

As seen in the picture below the installation is from development stage and it is not fastened and for a more permanent solution this needs to be mounted more properly.

The current device has not been tested in a heated sauna so there might be a need to look at another solution when it comes to installation. It might require the FiPy to be placed outside of the sauna and other sensors connected with longer cables to it that are then put inside the sauna. For temperature possible options could be a waterproof DS18B20 sensor or a DHT22 that should manage the heat.

![Easy assembly](/img/the_device.jpg)
Fig. 2. The device assembled

### Platforms and infrastructure

The aim in this project was to explore LoRaWAN and if I would not be able use LoRaWAN then I had the LTE network option since support for that network is included in the FiPy board. Luckily I was able to use LoRaWAN and therefore did not explore the LTE option in this project.

When searching for a LoRa platform to use where I live I found two options, [Helium](https://www.helium.com/) and [The Things network](https://www.thethingsnetwork.org/),TTN. It looked really promising with Helium according to their coverage map with gateways close to were I live but it turned out to not be that easy in reality. I did not get any connection to Helium when I tried.

Another person attending the same course knew a neighbor to me and he plugged in his TTN gateway and I was able to get a connection to TTN. This made the choice of platform easy.

The Things Network and more specific the The Things Stack Community Edition is a cloud based service that enables people to connect and manage gateways and IoT devices. It is free to use but there is a limitation in how much data you are allowed to transfer over the network or more specific how much airtime you can use. More data uses more airtime so there is a need to keep the data you send to minimum. In this project the air time is less than 0.07 seconds per transmit and the limit is 30 seconds per day (24 hours). There is also no uptime guarantee and is therefore not recommended for commercial use.

TTN has a number of APIs like HTTP and MQTT integrations and there is also a storage integration that allows you to store data from your devices for up to 30 days on the TTN servers.

LoRaWAN is a low-power, wide area networking protocol were the data from the devices are sent over radio(different world regions use different frequency plans, e.g. 863-870 MHz for Europe, 902-928 MHz for North America, etc.) to the gateway and from there over the internet to the TTN servers. From there the data can be fetched from or pushed directly to a receiving system.

For the web server part in my setup I use a web hotel where my domain is hosted and there I have access to databases(MariaDB) and PHP support.

![Platform and infrastructure](/img/platform.jpg)

Fig. 3. Platform and infrastructure

### The code

I only did the very basics to get this working and there are no things in current code to brag about so the below code is the complete main.py file. I have also two lines of code in boot.py to disable LTE.

In the first part I handle the imports of libraries, set the deepsleep time and handle the connection to LoRa. I use the nvram_restore to avoid performing the join request every time the device wakes up. I had some issues getting that to work  but finally got it working but I need to restructure the code a bit when I have time. :)

As a simple diagnostics I let the built in RGB led blink until there is a LoRa connection established and then turn it solid green until the device go to deepsleep and it is turned off.

```python=
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
```
In the second part of the main.py file i handle the reading of sensor data, rounding the values to one decimal, converting values to float and finally package the data using ustruct.pack and sending the data. In the end of the file I store the LoRa state using nvram_save and put the device in deepsleep.

```python=
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
```

### The physical network layer

Data that is sent from the device is temperature, humidity, batter percentage and battery voltage. The data is sent every 15 minutes over LoRaWAN.

When data is arriving at TTN a webhook is sending the data to the web server and the receiving PHP script decodes the json formatted data and stores it in a MariaDB.

I tried both the storage integration and the HTTP solution available on TTN but failed to get them working and therefore the choice was using the webhook solution. It is an easy task to set it up on the TTN console, you only need to provide an ID, what format you want the data to be sent in and the URL to the receiving endpoint, in my case the PHP script on my web server.

The MariaDB setup is very simple with one table containing columns for the data received from the device.

On the web server there are two PHP scripts, one that receives the data from the webhook and stores the data in the database and one script that reads the last row in the database and generates a HTML web page that displays the values. The reason why I choose a MariaDB and PHP scripts is that it was already available on my web server and I felt comfortable using it.

The alternatives to LoRaWAN could be WiFi but the sauna is to far away from any WiFi network and since I got LoRaWAN coverage I did not evaluate LTE that most likely could have been an option.

One issue I had was power consumption and I struggled a bit to find a working solution. I read that for the FiPy the LTE is always activated at boot so I disabled this in my boot.py file. From start I was using the machine.deepsleep function but battery lifetime was very limited, less than 24 hours. After some more research I found that machine.deepsleep did not put the Pysense board to sleep and I therefore needed to use the specific Pysense function go_to_sleep that did the trick and extended the battery  life by several days. For a more permanent solution I would go for a battery with higher mAh spec to extend time between every charge or even use a mobile charger to provide constant power. I would also do measurements on the actual power consumption on different configurations.

### Visualisation and user interface

The temperature and humidity data is presented on a website by a PHP script when a user views the webiste. The script opens a connection to the MariaDB and gets the last row of data in the database and generates the HTML code.

![Website](/img/website.jpg)

Fig. 4. Website visualisation

At the moment the data is stored every time it is sent from the device to TTN and the website and this could be good for history but one solution could also be to only send data from the device if it has changed since last measurement, that would save both device battery, air-time and database storage.

A future development could also be to alert me when the battery needs to be charged.

### Finalizing the design

This project was really fun and motivating, I learned a lot even though I just scratched the surface of the included parts like LoRa, TTN, MicroPython and micro controllers and sensors. I will definitely continue this project to get it fully working and deployed in the sauna and the data published on the sauna booking site.

As seen in the pictures below this is probably not the "final final" design and placement but the real sauna season is starting and I will continue the project even though the course is over.

![Device in sauna](/img/device_on_wall_1.jpg)

Fig. 5. Device in sauna

![Device in sauna](/img/device_on_wall_2.jpg)

Fig. 6. Device in sauna with a view

---
