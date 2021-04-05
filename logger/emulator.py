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

# relevant for charging/discharging
Command1 = bytearray(b'\x01\x03\x01\x02\x00\x10\xe4\x3a')
# 5% SOC energy saving mode
#Reply1 = bytearray(b'\x01\x03\x20\x08\xEE\x00\x00\x0F\x78\x00\x00\x10\xEE\x00\x00\x19\x17\x00\x00\xF3\x07\xFF\xFF\x03\x1A\x00\x00\x00\x00\x00\x00\x01\xF4\x00\x00\x1C\x56')
# 44 % SOC discharging
Reply1 = bytearray(b'\x01\x03\x20\x08\xe6\x00\x00\x0f\x6a\x00\x00\xff\x67\xff\xff\x1c\x0e\x00\x00\xe8\x6a\xff\xff\xff\xe7\xff\xff\x00\x00\x00\x00\x01\xf4\x00\x00\x93\xd9')


Command2 = bytearray(b'\x01\x03\x01\x1e\x00\x2a\xa5\xef')
# 5% SOC energy saving mode
Reply2 = bytearray(b'\x01\x03\x54\x0F\x73\x00\x00\x08\xF1\x00\x00\x06\xE5\x00\x00\x07\x28\x00\x00\x0E\xC1\x00\x00\xF3\x19\xFF\xFF\x01\xE5\x00\x00\x0F\x76\x00\x00\x08\xE6\x00\x00\x00\xE0\x00\x00\x00\x32\x00\x00\x00\xBB\x00\x00\x00\xB4\x00\x00\x01\x10\x00\x00\x0F\x80\x00\x00\x08\xF5\x00\x00\x04\xF5\x00\x00\x09\x92\x00\x00\x09\x9A\x00\x00\xFF\x3A\xFF\xFF\x03\xE5\x00\x00\x9F\x4D')


Command3 = bytearray(b'\x01\x03\x04\x00\x00\x10\x45\x36')
# 5% SOC energy saving mode
Reply3 = bytearray(b'\x01\x03\x20\x0F\x08\x00\x00\x02\xE8\x00\x00\x00\x5E\x00\x00\x02\xC9\x00\x00\x02\x5D\x00\x00\x00\x03\x00\x00\x07\xDF\x00\x00\x00\x98\x00\x00\x40\xB7')

ser = serial.Serial(
    port='COM6',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=15)

# debug stuff
print("Connected to: " + ser.portstr)

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

                # reply to request
                if bytearray(MSG) == Command1:
                    ser.write(Reply1)
                    print("Command 1-2")

                if bytearray(MSG) == Command2:
                    ser.write(Reply2)
                    print("Command 1-30")

                if bytearray(MSG) == Command3:
                    ser.write(Reply3)
                    print("Command 4-0")



            messageFound = False
            MSG = []
            byteCounter = 0


    #print(strftime("%Y-%m-%d_%H-%M %S",gmtime()) + ": " + repr(ser_bytes))
    #f.write(strftime("%Y-%m-%d_%H-%M %S",gmtime()) + ": " + repr(ser_bytes))

ser.close()
#f.close()

print("File + Port closed")