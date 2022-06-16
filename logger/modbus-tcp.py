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
mqtt_client =mqtt.Client("bossMQTT")
mqtt_client.connect("192.168.21.23", port=1883, keepalive=60, bind_address="")

for x in range(20000):
    
    response = client.read_holding_registers(address=0x5B00, count=0x3E, unit=1)
    
    if hasattr(response, "registers"):
        # -----------
        #power
        p1 = np.int32(np.left_shift(np.int16(response.registers[0x16]),16) | np.int32(response.registers[0x17])) / np.int32(100)
        p2 = np.int32(np.left_shift(np.int16(response.registers[0x18]),16) | np.int32(response.registers[0x19])) / np.int32(100)
        p3 = np.int32(np.left_shift(np.int16(response.registers[0x1A]),16) | np.int32(response.registers[0x1B])) / np.int32(100)
        psum = np.int32(np.left_shift(np.int16(response.registers[0x14]),16) | np.int32(response.registers[0x15])) / np.int32(100)
            
        mqtt_client.publish("smartmeter/p1", payload=p1)
        mqtt_client.publish("smartmeter/p2", payload=p2)
        mqtt_client.publish("smartmeter/p3", payload=p3)
        mqtt_client.publish("smartmeter/psum", payload=(psum))

        # # -----------
        # # voltages
        v1 = ((response.registers[0x0] << 16) | response.registers[0x1]) / 10
        v2 = ((response.registers[0x2] << 16) | response.registers[0x3]) / 10
        v3 = ((response.registers[0x4] << 16) | response.registers[0x5]) / 10

        mqtt_client.publish("smartmeter/v1", payload=v1)
        mqtt_client.publish("smartmeter/v2", payload=v2)
        mqtt_client.publish("smartmeter/v3", payload=v3)

        #Phase current
        c1 = ((response.registers[0x0C] << 16) | response.registers[0x0D]) / 100.0 * np.sign(p1)
        c2 = ((response.registers[0x0E] << 16) | response.registers[0x0F]) / 100.0 * np.sign(p2)
        c3 = ((response.registers[0x10] << 16) | response.registers[0x11]) / 100.0 * np.sign(p3)
        
        mqtt_client.publish("smartmeter/c1", payload=c1)
        mqtt_client.publish("smartmeter/c2", payload=c2)
        mqtt_client.publish("smartmeter/c3", payload=c3)
        
        # power factor
        pf = np.int16(response.registers[0x3A])/1000
        pf1 = np.int16(response.registers[0x3B])/1000
        pf2 = np.int16(response.registers[0x3C])/1000
        pf3 = np.int16(response.registers[0x3D])/1000
        
        mqtt_client.publish("smartmeter/pf", payload=pf)
        mqtt_client.publish("smartmeter/pf1", payload=pf1)
        mqtt_client.publish("smartmeter/pf2", payload=pf2)
        mqtt_client.publish("smartmeter/pf3", payload=pf3)
    
    response = client.read_holding_registers(address=0x5000, count=0x08, unit=1)
    
    if hasattr(response, "registers"):
        # energy forward
        ef = (np.left_shift(response.registers[0x00],48) | np.left_shift(response.registers[0x01],32) | np.left_shift(response.registers[0x02],16) | response.registers[0x03]) / 1000.0
        ee = (np.left_shift(response.registers[0x04],48) | np.left_shift(response.registers[0x05],32) | np.left_shift(response.registers[0x06],16) | response.registers[0x07]) / 1000.0
       
        mqtt_client.publish("smartmeter/ef", payload=ef)
        mqtt_client.publish("smartmeter/ee", payload=ee)
        
    response = client.read_holding_registers(address=0x5460, count=0x18, unit=1)
    if hasattr(response, "registers"):
        
        ef1 = (np.left_shift(response.registers[0x0],48) | np.left_shift(response.registers[0x01],32) | np.left_shift(response.registers[0x02],16) | response.registers[0x03]) / 1000.0
        ef2 = (np.left_shift(response.registers[0x04],48) | np.left_shift(response.registers[0x05],32) | np.left_shift(response.registers[0x06],16) | response.registers[0x07]) / 1000.0
        ef3 = (np.left_shift(response.registers[0x08],48) | np.left_shift(response.registers[0x09],32) | np.left_shift(response.registers[0x0A],16) | response.registers[0x0B]) / 1000.0

        mqtt_client.publish("smartmeter/ef1", payload=ef1)
        mqtt_client.publish("smartmeter/ef2", payload=ef2)
        mqtt_client.publish("smartmeter/ef3", payload=ef3)
        
        ee1 = (np.left_shift(response.registers[0x0C],48) | np.left_shift(response.registers[0x0D],32) | np.left_shift(response.registers[0x0E],16) | response.registers[0x0F]) / 1000.0
        ee2 = (np.left_shift(response.registers[0x10],48) | np.left_shift(response.registers[0x11],32) | np.left_shift(response.registers[0x12],16) | response.registers[0x13]) / 1000.0
        ee3 = (np.left_shift(response.registers[0x14],48) | np.left_shift(response.registers[0x15],32) | np.left_shift(response.registers[0x16],16) | response.registers[0x17]) / 1000.0

        mqtt_client.publish("smartmeter/ee1", payload=ee1)
        mqtt_client.publish("smartmeter/ee2", payload=ee2)
        mqtt_client.publish("smartmeter/ee3", payload=ee3)

client.close()