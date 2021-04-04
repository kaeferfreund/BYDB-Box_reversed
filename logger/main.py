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
gotLength = False
MSG = []
byteCounter = 0
REQ = []

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
            #print("MSG to BYD")
    else:
        MSG.append(ord(ser_bytes))
        byteCounter = byteCounter + 1

        if byteCounter == 7:
            data = MSG[0:6]
            crc = Crc16Modbus.calc(data)

            if MSG[6] == crc%256 and MSG[7] == crc/256:
                #print("Request recieved")
                #print("CRC - OK: (" + str(crc % 256) + ", " + str(crc / 256)+")")
                #print("REQ: " + str(MSG))
                #print("Register: " )

                messageFound = False
                REQ = list(MSG)
                MSG = 0
                byteCounter = 0
            else:
                #print("found reply")
                #print(" ->Length: " + str(MSG[2]))
                gotLength = True
        if gotLength:
            msgLen = 2 + MSG[2] + 2
            if byteCounter == msgLen:
                cleanMSG = MSG[0:msgLen - 1]
                crc = Crc16Modbus.calc(cleanMSG)
                #print("CRC OK: (" + str(crc % 256) + ", " + str(crc / 256) + ")")

                if MSG[msgLen-1] == crc % 256 and MSG[msgLen] == crc / 256:

                    # data does not contain addr, length and crc
                    data = cleanMSG[3:]

                    converted = []
                    for i in range(0, len(data)):
                        if(i%2 == 0):
                            result = (data[i] * 256) + data[i + 1]
                            if (result > 32768):
                                result = result - 65536
                            # if result == 13:
                            # print("FOUND 13")
                            converted.append(result)
                    if int(REQ[3]) == 30:
                        print("REQ: " + str(REQ))
                        #print("D " + str(data))
                        print("C "  +str(converted))

                    messageFound = False
                    MSG = 0
                    REQ = []
                    byteCounter = 0
                    gotLength = False


    #print(strftime("%Y-%m-%d_%H-%M %S",gmtime()) + ": " + repr(ser_bytes))
    #f.write(strftime("%Y-%m-%d_%H-%M %S",gmtime()) + ": " + repr(ser_bytes))

ser.close()
#f.close()

print("File + Port closed")