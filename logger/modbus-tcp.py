#!/usr/bin/python
from lib2to3.pytree import convert
import sys
# import os
# import time
# import getopt
# import socket
# import ConfigParser
# import struct
# import binascii
import ctypes
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer
import numpy as np
from collections import OrderedDict
import time
import paho.mqtt.client as mqtt


#Args in var schreiben

def printme( str ):
   "This prints a passed string into this function"
   print (str)
   return

client = ModbusClient("192.168.21.147", port=502, framer=ModbusRtuFramer)
mqtt_client =mqtt.Client("bossMQTT")
mqtt_client.connect("192.168.21.23", port=1883, keepalive=60, bind_address="")

for x in range(200):

    
    response = client.read_holding_registers(address=0x0, count=50, unit=1)

    #Phase power
    #p1 = ((response.registers[19] << 16) | response.registers[18]) / 10

    p1 = (np.left_shift(np.int16(response.registers[19]),16) | np.int16(response.registers[18])) / np.int32(10)
    p2 = (np.left_shift(np.int16(response.registers[21]),16) | np.int16(response.registers[20])) / np.int32(10)
    p3 = (np.left_shift(np.int16(response.registers[23]),16) | np.int16(response.registers[22])) / np.int32(10)
    
    print("p1: " , p1, "W")
    print("p2: " , p2, "W")
    print("p3: " , p3, "W")
    print("sum: ", p1+p2+p3 ,"W")
    
    mqtt_client.publish("smartmeter/p1", payload=p1)
    mqtt_client.publish("smartmeter/p2", payload=p2)
    mqtt_client.publish("smartmeter/p3", payload=p3)


    #Phase voltage
    v1 = ((response.registers[1] << 16) | response.registers[0]) / 10
    v2 = ((response.registers[3] << 16) | response.registers[2]) / 10
    v3 = ((response.registers[5] << 16) | response.registers[4]) / 10
    #print("v1: " , v1, "V")
    #print("v2: " , v2, "V")
    #print("v3: " , v3, "V")

    #Phase current
    c1 = ((response.registers[13] << 16) | response.registers[12]) / 1000
    c2 = ((response.registers[15] << 16) | response.registers[14]) / 1000
    c3 = ((response.registers[17] << 16) | response.registers[16]) / 1000
    #print("c1: " , c1, "A")
    #print("c2: " , c2, "A")
    #print("c3: " , c3, "A")

    p = ((response.registers[41] << 16) | response.registers[40]) / 10
    #print("P: " , p)

    #power factor
    pf1 = np.int16(response.registers[46])
    pf2 = np.int16(response.registers[47])
    pf3 = np.int16(response.registers[48])
    #pf3 = ((response.registers[51] << 16) | response.registers[50]) / 1000
    #print("pf1: " , pf1)
    #print("pf2: " , pf2)
    #print("pf3: " , pf3)

    response = client.read_holding_registers(address=0x32, count=50, unit=1)
    pf3 = ((response.registers[1] << 16) | response.registers[0]) / 1000
    pfs = ((response.registers[3] << 16) | response.registers[2]) / 1000
    #print("pf3: " , pf3)
    #print("pfs: " , pfs)

    time.sleep(1)
client.close()