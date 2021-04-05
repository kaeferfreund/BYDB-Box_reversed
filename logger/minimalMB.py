#!/usr/bin/env python3
import minimalmodbus

instrument = minimalmodbus.Instrument('COM6', 1)  # port name, slave address (in decimal)
instrument.serial.port = "COM6"
instrument.serial.baudrate = 9600


## Read temperature (PV = ProcessValue) ##
w1 = instrument.read_register(258, 4)  # Registernumber, number of decimals
w2 = instrument.read_register(260, 4)  # Registernumber, number of decimals
w3 = instrument.read_register(262, 4)  # Registernumber, number of decimals
w4 = instrument.read_register(264, 4)  # Registernumber, number of decimals
w5 = instrument.read_register(266, 4)  # Registernumber, number of decimals
w6 = instrument.read_register(268, 4)  # Registernumber, number of decimals
w7 = instrument.read_register(270, 4)  # Registernumber, number of decimals
w8 = instrument.read_register(272, 4)  # Registernumber, number of decimals
print(w1, w2, w3, w4, w5, w6, w7, w8)
print(w1+1, w2+10, w3+100, w4, w5, w6, w7, w8)

"""

C1 = instrument.read_register(0x400, 4)  # Registernumber, number of decimals
C2 = instrument.read_register(0x404, 4)  # Registernumber, number of decimals
C3 = instrument.read_register(0x40C, 4)  # Registernumber, number of decimals
#C4 = instrument.read_register(0x410, 4)  # Registernumber, number of decimals



print(C1, C2, C3)

"""
