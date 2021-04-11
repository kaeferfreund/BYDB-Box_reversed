#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial, json, codecs
import time
from crccheck.crc import Crc16Modbus

import struct

# simple serial logger by
# Manuel Cargnel
# (c) C2 Konzepte GbR
# 07-03-2021

Command1 = bytearray(b'\x01\x03\x01\x02\x00\x10\xe4\x3a')

# open serialPort
# please replace /dev/cu.usbserial-A50285BI with your actual device
# bitte ersetzen Sie /dev/cu.usbserial-A50285BI durch Ihr Gerät

ser = serial.Serial(
    port='/dev/cu.usbserial-AR0KMGSU',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=15)

# debug stuff
print("Connected to: " + ser.portstr)

# open log file
#f = codecs.open( strftime("%Y-%m-%d_%H-%M",gmtime()) + ".log", 'w')

ser.write(Command1)
time.sleep(0.1)

ser.close()