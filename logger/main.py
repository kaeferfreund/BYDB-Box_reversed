import serial, json, codecs
from time import gmtime, strftime
import struct

# simple serial logger by 
# Manuel Cargnel
# (c) C2 Konzepte GbR
# 17-10-2020

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

# logging loop
while ser.is_open:
    ser_bytes = ser.read()

    print(strftime("%Y-%m-%d_%H-%M %S",gmtime()) + ": " + repr(ser_bytes))
    f.write(strftime("%Y-%m-%d_%H-%M %S",gmtime()) + ": " + repr(ser_bytes))

ser.close()
f.close()

print("File + Port closed")