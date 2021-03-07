#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial, json, codecs
from time import gmtime, strftime
from crccheck.crc import Crc16Modbus

import struct

# simple serial logger by 
# Manuel Cargnel
# (c) C2 Konzepte GbR
# 17-10-2020

# Quick calculation


data = [01,03,01,02,00,16]
crc = Crc16Modbus.calc(data)
print("crc: "  + str(crc%256) +","+ str(crc/256))
# Result should be 228 + 58


# open serialPort
# please replace /dev/cu.usbserial-A50285BI with your actual device
# bitte ersetzen Sie /dev/cu.usbserial-A50285BI durch Ihr Gerät

ser = serial.Serial(
    port='/dev/cu.usbserial-A50285BI',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=15)

# debug stuff
print("Connected to: " + ser.portstr)

# open log file
f = codecs.open( strftime("%Y-%m-%d_%H-%M",gmtime()) + ".log", 'w')

firstByte = 00
secondByte = 00
messageFound = False
MSG = []
byteCounter = 0

# logging loop
while ser.is_open:
    ser_bytes = ser.read()

    if messageFound == False:
        secondByte = firstByte
        firstByte = ser_bytes

        if firstByte == 01 & secondByte == 03:
            messageFound = True
            MSG.append(firstByte)
            MSG.append(secondByte)
            byteCounter = 2
            print("MSG to BYD")
    else:
        MSG.append(ser_bytes)
        byteCounter = byteCounter + 1

        if byteCounter == 8:
            data = MSG
            crc = Crc16Modbus.calc(data)

            if MSG[7] == crc%256 & MSG[8] == crc/256:
                print("Anforderung an BYD empfangen")

    print(strftime("%Y-%m-%d_%H-%M %S",gmtime()) + ": " + repr(ser_bytes))
    f.write(strftime("%Y-%m-%d_%H-%M %S",gmtime()) + ": " + repr(ser_bytes))

ser.close()
f.close()

print("File + Port closed")