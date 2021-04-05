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

def intToBytes(number):
    byte_array = []
    while number != 0:
        byte_array = [number % 256] + byte_array
        number = number // 256
    return byte_array

def toInt(hB, lB):
    result = (hB * 256) + lB
    if (result > 32768):
        result = result - 65536
    return result

def toUInt(hB, lB):
    result = (hB * 256) + lB
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
gotLength = False
MSG = []
orgMSG = []
byteCounter = 0
REQ = []

# logging loop
while ser.is_open:
    ser_bytes = ser.read()

    if messageFound == False:
        secondByte = firstByte
        firstByte = ser_bytes
        #print(firstByte)

        if ord(firstByte) == 3 and ord(secondByte) == 1:
            messageFound = True
            MSG = []
            orgMSG = []
            MSG.append(ord(secondByte))
            MSG.append(ord(firstByte))
            orgMSG.append(secondByte)
            orgMSG.append(firstByte)
            byteCounter = 1
            #print("MSG to BYD")
    else:
        MSG.append(ord(ser_bytes))
        orgMSG.append(ser_bytes)
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
                MSG = []
                orgMSG = []
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

                    BE = []
                    LE = []

                    for i in range(0, len(data)-1):

                        if(i%2 == 0):
                            result = toInt(data[i], data[i + 1])
                            LE.append(result)

                        if(i%4 == 0):

                            ba = []
                            ba.append(orgMSG[i+5]) #A -3
                            ba.append(orgMSG[i+6]) #B- 4
                            ba.append(orgMSG[i+3]) #C - 5
                            ba.append(orgMSG[i+4]) #D - 6

                            #print ' '.join(format(ord(x), '02x') for x in ba)
                            #result = struct.unpack("!i",bytearray(ba))[0]/10000.0
                            #result = toInt(hb, lb)

                            #print("hb: " + hex(hb) + " - lb: " + hex(lb) + " - res: " + str(result))

                            BE.append(result)

                    if int(REQ[3]) == 2:
                        #print ' '.join(format(x, '02x') for x in REQ)
                        #print ' '.join(format(x, '02x') for x in data)
                        print ' '.join(format(ord(x), '02x') for x in orgMSG)

                        #print("BE: " + str(BE))
                        #print("LE: " + str(LE))

                    messageFound = False
                    MSG = []
                    orgMSG = []
                    REQ = []
                    byteCounter = 0
                    gotLength = False


    #print(strftime("%Y-%m-%d_%H-%M %S",gmtime()) + ": " + repr(ser_bytes))
    #f.write(strftime("%Y-%m-%d_%H-%M %S",gmtime()) + ": " + repr(ser_bytes))

ser.close()
#f.close()

print("File + Port closed")