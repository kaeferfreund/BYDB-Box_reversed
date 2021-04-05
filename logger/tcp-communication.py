#!/usr/bin/env python

import socket, sys, select
import struct
from time import sleep

def toInt(hB, lB):
    result = (hB * 256) + lB
    if (result > 32768):
        result = result - 65536
    return result

TCP_IP = "192.168.56.100"
#TCP_IP = "8.8.8.8"
TCP_PORT = 8080
#MESSAGE = bytearray("0103 00 00 00 66c5e0")
BUFFER_SIZE = 4048

Fronius = bytearray(b'\x01\x03\x01\x02\x00\x10\xe4\x3a')

BIN1 = bytearray(b'\x01\x03\x00\x00\x00\x66\xc5\xe0')
BIN2 = bytearray(b'\x01\x03\x05\x00\x00\x19\x84\xcc')

BIN = BIN2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

try:
    s.sendall(BIN)

    data = s.recv(1024)
    print ("%: " + str(toInt(ord(data[3]), ord(data[4]))))
    print >> sys.stderr, 'received "%s"' % repr(data)

finally:
    print >> sys.stderr, 'closing socket'
    s.close()