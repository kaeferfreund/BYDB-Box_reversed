import serial, json, codecs
import time
from crccheck.crc import Crc16Modbus
#55 AA 01 FF 00 00 FF

# JKBMS Communication first steps

def toInt(hB, lB):
    result = (hB * 256) + lB
    if (result > 32768):
        result = result - 65536
    return result

Command1 = bytearray(b'\x55\xaa\x01\xff\x00\x00\xff')

ser = serial.Serial(
    port='COM6',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=15)

print("serial sent")
ser.write(Command1)
time.sleep(1)
count = 0
message = []

while ser.is_open:
    count = count + 1
    ser_bytes = ser.read()
    #print(repr(ser_bytes))
    message.append(ord(ser_bytes))

    if(count == 74):
        voltages = []

        for x in range(0, 13):
            voltages.append(toInt(message[23+(x*2)], message[24+(x*2)]))
        print("Voltages: " + str(voltages))
        print("Temp: " + str(toInt(message[71], message[72])))

        count = 0
        ser.write(Command1)
        time.sleep(1)
        count = 0
        message = []

