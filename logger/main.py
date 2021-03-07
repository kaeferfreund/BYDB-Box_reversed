#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial, json, codecs
from time import gmtime, strftime
from crccheck.crc import Crc16Modbus

import struct

# simple serial logger by 
# Manuel Cargnel
# (c) C2 Konzepte GbR
# 07-03-2021


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
#f = codecs.open( strftime("%Y-%m-%d_%H-%M",gmtime()) + ".log", 'w')

firstByte = 0
secondByte = 0
messageFound = False
MSG = []
byteCounter = 0

# logging loop
while ser.is_open:
    ser_bytes = ser.read()

    if messageFound == False:
        secondByte = firstByte
        firstByte = ord(ser_bytes)
        #print(firstByte)

        if firstByte == 3 and secondByte == 1:
            messageFound = True
            MSG = []
            MSG.append(secondByte)
            MSG.append(firstByte)
            byteCounter = 1
            print("MSG to BYD")
    else:
        MSG.append(ord(ser_bytes))
        byteCounter = byteCounter + 1

        if byteCounter >= 8:
            data = MSG[0:6]
            crc = Crc16Modbus.calc(data)

            if MSG[6] == crc%256 and MSG[7] == crc/256:
                print("Request recieved")
                print("CRC - OK: " + str(crc % 256) + ", " + str(crc / 256))
                print("MSG: " + str(MSG))
                print("Register: " )

                messageFound = False
                MSG = 0
                byteCounter = 0
            #else:
            #    print("found reply")
            #    print("Length: " + str(MSG[3]))

    #print(strftime("%Y-%m-%d_%H-%M %S",gmtime()) + ": " + repr(ser_bytes))
    #f.write(strftime("%Y-%m-%d_%H-%M %S",gmtime()) + ": " + repr(ser_bytes))

ser.close()
#f.close()

print("File + Port closed")