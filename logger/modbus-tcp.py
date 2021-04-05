#!/usr/bin/python
import sys
import os
import time
import getopt
import socket
import ConfigParser
import struct
import binascii

from pymodbus.client.sync import ModbusTcpClient as ModbusClient

active_power = 1

client = ModbusClient("192.168.56.100", port=8080, unit_id=1)
client.connect()
if client.connect():
    print("connected")
    time.sleep(1)
    rr = client.read_holding_registers(0x00, 0x66, unit=1)

    #active_power = rr.registers[1]
    print("power" + str(rr))
