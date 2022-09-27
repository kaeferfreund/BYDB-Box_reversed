#!/usr/bin/python
from lib2to3.pytree import convert
import sys
import ctypes
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer
import numpy as np
from collections import OrderedDict
import paho.mqtt.client as mqtt


client = ModbusClient("192.168.21.147", port=502, framer=ModbusRtuFramer)
mqtt_client = mqtt.Client("bossMQTT")
mqtt_client.connect("192.168.21.23", port=1883, keepalive=60, bind_address="")

p1_ = p2_ = p3_ = psum_ = 0
v1_ = v2_ = v3_ = 0
c1_ = c2_ = c3_ = 0
pf_ = pf1_ = pf2_ = pf3_ = 0
ee_ = ef_ = 0
ef1_ = ef2_ = ef3_ = 0
ee1_ = ee2_ = ee3_ = 0
f_ = 0
phySq_ = 0

for x in range(2000000):

    response = client.read_holding_registers(
        address=0x00, count=0x34, unit=1)
    

    if hasattr(response, "registers"):
        
        # -----------
        # power
        p1 = np.int32(np.left_shift(np.int16(response.registers[0x13]), 16) | np.int32(
            response.registers[0x12])) / 10.0
        p2 = np.int32(np.left_shift(np.int16(response.registers[0x015]), 16) | np.int32(
            response.registers[0x14])) / 10.0
        p3 = np.int32(np.left_shift(np.int16(response.registers[0x17]), 16) | np.int32(
            response.registers[0x16])) / 10.0
        psum = np.int32(np.left_shift(np.int16(response.registers[0x29]), 16) | np.int32(
            response.registers[0x28])) / 10.0

        if(p1 != p1_):
            mqtt_client.publish("smartmeter/p1", payload=p1)
            p1_ = p1
        if(p2 != p2_):
            mqtt_client.publish("smartmeter/p2", payload=p2)
            p2_ = p2
        if(p3 != p3_):
            mqtt_client.publish("smartmeter/p3", payload=p3)
            p3_ = p3
        if(psum != psum_):
            mqtt_client.publish("smartmeter/psum", payload=psum)
            psum_ = psum

    #     # # -----------
    #     # # voltages

        v1 = ((response.registers[0x1] << 16) | response.registers[0x0]) / 10.0
        v2 = ((response.registers[0x3] << 16) | response.registers[0x2]) / 10.0
        v3 = ((response.registers[0x5] << 16) | response.registers[0x4]) / 10.0

        if(v1 != v1_):
            mqtt_client.publish("smartmeter/v1", payload=v1)
            v1_ = v1
        if(v2 != v2_):
            mqtt_client.publish("smartmeter/v2", payload=v2)
            v2_ = v2
        if(v3 != v3_):
            mqtt_client.publish("smartmeter/v3", payload=v3)
            v3_ = v3

    #     # Phase current
        c1 = ((response.registers[0x0D] << 16) |
              response.registers[0x0C]) / 1000.0 
        c2 = ((response.registers[0x0F] << 16) |
              response.registers[0x0E]) / 1000.0
        c3 = ((response.registers[0x11] << 16) |
              response.registers[0x10])  / 1000.0

        if(c1 != c1_):
            mqtt_client.publish("smartmeter/c1", payload=c1)
            c1_ = c1
        if(c2 != c2_):
            mqtt_client.publish("smartmeter/c2", payload=c2)
            c2_ = c2
        if(c3 != c3_):
            mqtt_client.publish("smartmeter/c3", payload=c3)
            c3_ = c3

    #     # power factor
        pf = np.int16(response.registers[0x2E])/1000.0
        pf1 = np.int16(response.registers[0x2F])/1000.0
        pf2 = np.int16(response.registers[0x30])/1000.0
        pf3 = np.int16(response.registers[0x31])/1000.0

        if(pf != pf_):
            mqtt_client.publish("smartmeter/pf", payload=pf)
            pf_ = pf
        if(pf1 != pf1_):
            mqtt_client.publish("smartmeter/pf1", payload=pf1)
            pf1_ = pf1
        if(pf2 != pf2_):
            mqtt_client.publish("smartmeter/pf2", payload=pf2)
            pf2_ = pf2
        if(pf3 != pf3_):
            mqtt_client.publish("smartmeter/pf3", payload=pf3)
            pf3_ = pf3

        # frequency
        f = np.int16(response.registers[0x33])/10.0

        if(f != f_):
            mqtt_client.publish("smartmeter/f", payload=f)
            f_ = f
            
        phySq = np.int16(response.registers[0x32])
            
        if(phySq != phySq_):
            mqtt_client.publish("smartmeter/phySq", payload=int(phySq))
            phySq_ = phySq
            
            
    start2 = 0x34
            
    response = client.read_holding_registers(
        address=start2, count=0x50-start2, unit=1)

    if hasattr(response, "registers"):
        # energy forward
        ef = ((response.registers[0x35-start2] << 16) |
              response.registers[0x34-start2])  / 10.0
        ee = ((response.registers[0x4F-start2] << 16) |
              response.registers[0x4E-start2])  / 10.0

        if(ef != ef_ and ef != 0):
            mqtt_client.publish("smartmeter/ef", payload=ef)
            ef_ = ef
        if(ee != ee_ and ee != 0):
            mqtt_client.publish("smartmeter/ee", payload=ee)
            ee_ = ee

        ef1 =  ((response.registers[0x41-start2] << 16) |
              response.registers[0x40-start2])  / 10.0
        ef2 =  ((response.registers[0x43-start2] << 16) |
              response.registers[0x42-start2])  / 10.0
        ef3 =((response.registers[0x45-start2] << 16) |
              response.registers[0x44-start2])  / 10.0
        
        if(ef1 != ef1_ and ef1 != 0):
            mqtt_client.publish("smartmeter/ef1", payload=ef1)
            ef1_ = ef1
        if(ef2 != ef2_ and ef2 != 0):
            mqtt_client.publish("smartmeter/ef2", payload=ef2)
            ef2_ = ef2
        if(ef3 != ef3_ and ef3 != 0):
            mqtt_client.publish("smartmeter/ef3", payload=ef3)
            ef3_ = ef3

        # ee1 = ((response.registers[0x41-start2] << 16) |
        #       response.registers[0x40-start2])  / 10.0
        # ee2 = ((response.registers[0x43-start2] << 16) |
        #       response.registers[0x42-start2])  / 10.0
        # ee3 = ((response.registers[0x45-start2] << 16) |
        #       response.registers[0x44-start2])  / 10.0
        
        # if(ee1 != ee1_ and ee1 != 0):
        #     mqtt_client.publish("smartmeter/ee1", payload=ee1)
        #     ee1_ = ee1
        # if(ee2 != ee2_ and ee2 != 0):
        #     mqtt_client.publish("smartmeter/ee2", payload=ee2)
        #     ee2_ = ee2
        # if(ee3 != ee3_ and ee3 != 0):
        #     mqtt_client.publish("smartmeter/ee3", payload=ee3)
        #     ee3_ = ee3

client.close()
