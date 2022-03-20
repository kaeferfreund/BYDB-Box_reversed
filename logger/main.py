#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial, json, codecs
from time import gmtime, strftime
from crccheck.crc import Crc16Modbus
import Queue

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

Command1 = bytearray(b'\x15\x03\x01\x91\x00\x01\xd7\x0f')
Command2 = bytearray(b'\x15\x03\x01\x2c\x00\x18\x86\xe1')
Command3 = bytearray(b'\x01\x03\x04\x00\x00\x10\x45\x36')
Command4 = bytearray(b'\x15\x10\x01\x91\x00\x01\x52\xcc')

# open serialPort
# please replace /dev/cu.usbserial-A50285BI with your actual device
# bitte ersetzen Sie /dev/cu.usbserial-A50285BI durch Ihr Gerät

ser = serial.Serial(
    port='COM9',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=15)

# debug stuff
print("Connected to: " + ser.portstr)

# open log file
#f = codecs.open( strftime("%Y-%m-%d_%H-%M",gmtime()) + ".log", 'w')

inQ = q1 = Queue.Queue()

messageFound = False
request = []
replyByteCount = 0

# logging loop
while ser.is_open:
    ser_bytes = ser.read()
    inQ.put(ser_bytes)

    # we are looking for a request, which is 7 bytes long
    if(messageFound == False and inQ.qsize() == 8):
        #calc CRC
        inQarray = inQ.queue
        inQNum = [ord(x) for x in inQarray]
        data = inQNum[:6]
        crc = Crc16Modbus.calc(data)

        # check CRC
        if inQNum[6] == crc % 256 and inQNum[7] == crc / 256:
            #print("CRC ok")
            #print("REQ: "),
            #print ' '.join(format(x, '02x') for x in inQNum)

            #clear queue
            request = inQNum
            inQ = Queue.Queue()

            address = inQNum[0]

            if(address == 0x1):
                i = 1
                #print ("SmartMeter")
            if(address == 0x15):
                i = 1
                print ' '.join(format(x, '02x') for x in inQNum)

            messageFound = True
        else:
            inQ.get()
    if(messageFound):
        # now handly reply

        # get length of reply
        if inQ.qsize() == 3:
            replyByteCount = ord(ser_bytes)
            #print("byteCount: " + str(int(replyByteCount)))
        if replyByteCount > 0 and inQ.qsize() == replyByteCount+5:
            # check CRC
            inQarray = inQ.queue
            inQNum = [ord(x) for x in inQarray]
            data = inQNum[:replyByteCount+3]
            crc = Crc16Modbus.calc(data)

            # reset vars
            inQ = Queue.Queue()
            messageFound = False

            # handle message
            if inQNum[replyByteCount+3] == crc % 256 and inQNum[replyByteCount+4] == crc / 256:
                address = inQNum[0]
                #print("reply crc ok")

                if (address == 0x1):
                    i = 1
                    #print ("SmartMeter")
                if (address == 0x15):
                    i = 1
                    print ' '.join(format(x, '02x') for x in inQNum)

                if(bytearray(request) == Command2):
                    offset = 3
                    soc = toInt(inQNum[offset+6], inQNum[offset+7])/100.0
                    voltage = toInt(inQNum[offset+16], inQNum[offset+17])/10.0
                    power = toInt(inQNum[offset+18], inQNum[offset+19])
                    tMin = toInt(inQNum[offset+24], inQNum[offset+25])/10.0
                    tMax = toInt(inQNum[offset+26], inQNum[offset+27])/10.0
                    soh = toInt(inQNum[offset+46], inQNum[offset+47])/100.0
                    energyTroughputOut = ((inQNum[offset+40] << 24)|(inQNum[offset+41] << 16)|(inQNum[offset+42] << 8)|inQNum[offset+43])
                    energyTroughputIn = ((inQNum[offset+32] << 24)|(inQNum[offset+33] << 16)|(inQNum[offset+34] << 8)|inQNum[offset+35])
                    efficiency = energyTroughputOut/float(energyTroughputIn)
                    capacity = toInt(inQNum[offset+8], inQNum[offset+9])
                    energyStored = toInt(inQNum[offset+10], inQNum[offset+11])
                    bcuTemp = toInt(inQNum[offset+44], inQNum[offset+45])

                    print("bytes:" + str(replyByteCount) + " SOC: " + str(soc) + " Voltage: " + str(voltage) + " Power: " + str(power) + "W, ")
                    print("Efficiency: " + str(efficiency) + "%, " + " EnergyStored: "+ str(energyStored) + " TroughputOut: " + str(energyTroughputOut)  + " TroughputIn: " + str(energyTroughputIn) + " SOH: " + str(soh))
                    print("bcuTemp: " + str(bcuTemp/10.0) + " tMin: " + str(tMin) + " tMax: " + str(tMax) )
                    print ' '.join(format(x, '02x') for x in inQNum)
            else:
                print("reply CRC broken")
                if (bytearray(request) == Command4):
                    print "write reply"
                    print ' '.join(format(x, '02x') for x in inQNum)

""""
    # no request detected
    if messageFound == False:
        secondByte = firstByte
        firstByte = ser_bytes

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
    # found request        
    if messageFound == True:
        MSG.append(ord(ser_bytes))
        orgMSG.append(ser_bytes)
        byteCounter = byteCounter + 1

        if byteCounter == 7:
            data = MSG[0:6]
            crc = Crc16Modbus.calc(data)

            if MSG[6] == crc%256 and MSG[7] == crc/256:
                print("Request recieved")
                #print("CRC - OK: (" + str(crc % 256) + ", " + str(crc / 256)+")")

                messageFound = False
                REQ = list(MSG)
                MSG = []
                orgMSG = []
                byteCounter = 0

                print("REQ: "),
                print ' '.join(format(x, '02x') for x in REQ)
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

                    #if bytearray(REQ) == Command3:
                        #print ' '.join(format(x, '02x') for x in REQ)
                        #print ' '.join(format(x, '02x') for x in data)
                    #print ' '.join(format(ord(x), '02x') for x in orgMSG)
                        #print ' '.join(str(ord(x)) for x in orgMSG)

                        #print("BE: " + str(BE))
                        #print("LE: " + str(LE))
                    print">",
                    print("msglen: " + str(msgLen))

                    messageFound = False
                    MSG = []
                    orgMSG = []
                    REQ = []
                    byteCounter = 0
                    gotLength = False
                    
    if gotLength == False and byteCounter != 7:
        print("abc")
            #what now

    #print(strftime("%Y-%m-%d_%H-%M %S",gmtime()) + ": " + repr(ser_bytes))
    #f.write(strftime("%Y-%m-%d_%H-%M %S",gmtime()) + ": " + repr(ser_bytes))
"""

ser.close()
#f.close()

print("File + Port closed")