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

def toByteArray(array):
    result = bytearray()
    for b in array:
        result.append()



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

ser1 = serial.Serial(
    port='/dev/cu.usbserial-AR0K8QFG',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=15)

ser2 = serial.Serial(
    port='/dev/cu.usbserial-AR0KMSGU',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=15)

# debug stuff
print("Connected to: " + ser1.portstr)
print("Connected to: " + ser2.portstr)

# logging loop
while ser.is_open:

    ser_bytes = ser.read()

    if messageFound == False:
        secondByte = firstByte
        firstByte = ord(ser_bytes)
        print(firstByte)

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

        if byteCounter == 7:
            print("MSG: " + str(MSG))
            data = MSG[0:6]
            crc = Crc16Modbus.calc(data)

            if MSG[6] == crc%256 and MSG[7] == crc/256:
                print("Request recieved")
                print("CRC - OK: (" + str(crc % 256) + ", " + str(crc / 256)+")")
                print("REQ: " + str(MSG))

                #print("Register: " )

                # reply to request
                if bytearray(MSG) == Command1:
                    ser.write(Reply1)
                    print("Command 1-2")

                if bytearray(MSG) == Command2:
                    #ser.write(Reply2)
                    print("Command 1-30")

                if bytearray(MSG) == Command3:
                    #ser.write(Reply3)
                    print("Command 4-0")



            messageFound = False
            MSG = []
            byteCounter = 0


    #print(strftime("%Y-%m-%d_%H-%M %S",gmtime()) + ": " + repr(ser_bytes))
    #f.write(strftime("%Y-%m-%d_%H-%M %S",gmtime()) + ": " + repr(ser_bytes))

ser.close()
#f.close()

print("File + Port closed")