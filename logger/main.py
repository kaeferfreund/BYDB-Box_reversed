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


def toInt(hB, lB):
    result = (hB * 256) + lB
    if (result > 32768):
        result = result - 65536
    return result

def toFloat(hBI, lBI):
    hB = struct.pack("B", hBI)
    lB = struct.pack("B", lBI)

    bb = bytearray([hBI, lBI])
    print(repr(bb))

    bytes = repr(hB) + repr(lB)
    bytes = bytes.replace('\'', '')

    #result = struct.unpack('d', bb)[0]

    return 2# result

# open serialPort
# please replace /dev/cu.usbserial-A50285BI with your actual device
# bitte ersetzen Sie /dev/cu.usbserial-A50285BI durch Ihr Gerät

ser = serial.Serial(
    port='COM6',\
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
replyFound = False
gotLength = False
MSG = []
byteCounter = 0
REQ = []

# logging loop
while ser.is_open:
    ser_bytes = ser.read()

    # NO 0103 request here yet
    if gotLength == False and messageFound == False:
        secondByte = firstByte
        firstByte = ord(ser_bytes)
        #print(firstByte)

        if firstByte == 3 and secondByte == 1:
            messageFound = True
            MSG.append(secondByte)
            MSG.append(firstByte)
            byteCounter = 1
            print("MSG to BYD")
    # 0103 request was fount
    else:
        MSG.append(ord(ser_bytes))
        byteCounter = byteCounter + 1

        # request is complete
        if gotLength == False and byteCounter == 7:
            data = MSG[0:6]
            print("MSG" + str(MSG))
            crc = Crc16Modbus.calc(data)

            # check CRC
            if MSG[6] == int(crc%256) and MSG[7] == int(crc/256):
                #print("Request recieved")
                #print("CRC - OK: (" + str(crc % 256) + ", " + str(crc / 256)+")")
                print("REQ: " + str(MSG))
                #print("Register: " )

                REQ = list(MSG)
                MSG = []
                byteCounter = 0
            else:
                print("found reply")
                print(" ->Length: " + str(MSG[2]))
                msgLen = int(MSG[2] + 4)
                gotLength = True
                
        if gotLength:
            if (byteCounter-1) == msgLen:
                cleanMSG = MSG[0:msgLen - 1]
                crc = Crc16Modbus.calc(cleanMSG)
                print("MSG: " + str(MSG))
                print("CRC OK: (" + str(crc % 256) + ", " + str(crc / 256) + ")")

                if MSG[msgLen-1] == int(crc % 256) and MSG[msgLen] == int(crc / 256):

                    # data does not contain addr, length and crc
                    data = cleanMSG[3:]

                    converted = []
                    for i in range(0, len(data)):
                        if(i%2 == 0):

                            hB = data[i]
                            lB = data[i+1]

                            converted.append(toFloat(hB, lB))
                    if int(REQ[3]) == 2:
                        #print("REQ: " + str(REQ))
                        #print("D " + str(data))
                        print("C "  +str(converted))

                    messageFound = False
                    print("clear-")
                    MSG = []
                    REQ = []
                    byteCounter = 0
                    gotLength = False


    #print(strftime("%Y-%m-%d_%H-%M %S",gmtime()) + ": " + repr(ser_bytes))
    #f.write(strftime("%Y-%m-%d_%H-%M %S",gmtime()) + ": " + repr(ser_bytes))

ser.close()
#f.close()

print("File + Port closed")