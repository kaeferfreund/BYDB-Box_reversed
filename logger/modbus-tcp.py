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

for x in range(2000000):

    response = client.read_holding_registers(
        address=0x5B00, count=0x3E, unit=1)

    if hasattr(response, "registers"):
        # -----------
        # power
        p1 = np.int32(np.left_shift(np.int16(response.registers[0x16]), 16) | np.int32(
            response.registers[0x17])) / 100.0
        p2 = np.int32(np.left_shift(np.int16(response.registers[0x18]), 16) | np.int32(
            response.registers[0x19])) / 100.0
        p3 = np.int32(np.left_shift(np.int16(response.registers[0x1A]), 16) | np.int32(
            response.registers[0x1B])) / 100.0
        psum = np.int32(np.left_shift(np.int16(response.registers[0x14]), 16) | np.int32(
            response.registers[0x15])) / 100.0

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

        # # -----------
        # # voltages

        v1 = ((response.registers[0x0] << 16) | response.registers[0x1]) / 10.0
        v2 = ((response.registers[0x2] << 16) | response.registers[0x3]) / 10.0
        v3 = ((response.registers[0x4] << 16) | response.registers[0x5]) / 10.0

        if(v1 != v1_):
            mqtt_client.publish("smartmeter/v1", payload=v1)
            v1_ = v1
        if(v2 != v2_):
            mqtt_client.publish("smartmeter/v2", payload=v2)
            v2_ = v2
        if(v3 != v3_):
            mqtt_client.publish("smartmeter/v3", payload=v3)
            v3_ = v3

        # Phase current
        c1 = ((response.registers[0x0C] << 16) |
              response.registers[0x0D]) / 100.0 * np.sign(p1)
        c2 = ((response.registers[0x0E] << 16) |
              response.registers[0x0F]) / 100.0 * np.sign(p2)
        c3 = ((response.registers[0x10] << 16) |
              response.registers[0x11]) / 100.0 * np.sign(p3)

        if(c1 != c1_):
            mqtt_client.publish("smartmeter/c1", payload=c1)
            c1_ = c1
        if(c2 != c2_):
            mqtt_client.publish("smartmeter/c2", payload=c2)
            c2_ = c2
        if(c3 != c3_):
            mqtt_client.publish("smartmeter/c3", payload=c3)
            c3_ = c3

        # power factor
        pf = np.int16(response.registers[0x3A])/1000.0
        pf1 = np.int16(response.registers[0x3B])/1000.0
        pf2 = np.int16(response.registers[0x3C])/1000.0
        pf3 = np.int16(response.registers[0x3D])/1000.0

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
        f = np.int16(response.registers[0x2C])/100.0

        if(f != f_):
            mqtt_client.publish("smartmeter/f", payload=f)
            f_ = f

    response = client.read_holding_registers(
        address=0x5000, count=0x08, unit=1)

    if hasattr(response, "registers"):
        # energy forward
        ef = (np.left_shift(response.registers[0x00], 48) | np.left_shift(response.registers[0x01], 32) | np.left_shift(
            response.registers[0x02], 16) | response.registers[0x03]) / 100.0
        ee = (np.left_shift(response.registers[0x04], 48) | np.left_shift(response.registers[0x05], 32) | np.left_shift(
            response.registers[0x06], 16) | response.registers[0x07]) / 100.0

        if(ef != ef_):
            mqtt_client.publish("smartmeter/ef", payload=ef)
            ef_ = ef
        if(ee != ee_):
            mqtt_client.publish("smartmeter/ee", payload=ee)
            ee_ = ee

    response = client.read_holding_registers(
        address=0x5460, count=0x18, unit=1)
    if hasattr(response, "registers"):

        ef1 = (np.left_shift(response.registers[0x0], 48) | np.left_shift(response.registers[0x01], 32) | np.left_shift(
            response.registers[0x02], 16) | response.registers[0x03]) / 100.0
        ef2 = (np.left_shift(response.registers[0x04], 48) | np.left_shift(
            response.registers[0x05], 32) | np.left_shift(response.registers[0x06], 16) | response.registers[0x07]) / 100.0
        ef3 = (np.left_shift(response.registers[0x08], 48) | np.left_shift(
            response.registers[0x09], 32) | np.left_shift(response.registers[0x0A], 16) | response.registers[0x0B]) / 100.0

        if(ef1 != ef1_):
            mqtt_client.publish("smartmeter/ef1", payload=ef1)
            ef1_ = ef1
        if(ef2 != ef2_):
            mqtt_client.publish("smartmeter/ef2", payload=ef2)
            ef2_ = ef2
        if(ef3 != ef3_):
            mqtt_client.publish("smartmeter/ef3", payload=ef3)
            ef3_ = ef3

        ee1 = (np.left_shift(response.registers[0x0C], 48) | np.left_shift(
            response.registers[0x0D], 32) | np.left_shift(response.registers[0x0E], 16) | response.registers[0x0F]) / 100.0
        ee2 = (np.left_shift(response.registers[0x10], 48) | np.left_shift(
            response.registers[0x11], 32) | np.left_shift(response.registers[0x12], 16) | response.registers[0x13]) / 100.0
        ee3 = (np.left_shift(response.registers[0x14], 48) | np.left_shift(
            response.registers[0x15], 32) | np.left_shift(response.registers[0x16], 16) | response.registers[0x17]) / 100.0

        if(ee1 != ee1_):
            mqtt_client.publish("smartmeter/ee1", payload=ee1)
            ee1_ = ee1
        if(ee2 != ee2_):
            mqtt_client.publish("smartmeter/ee2", payload=ee2)
            ee2_ = ee2
        if(ee3 != ee3_):
            mqtt_client.publish("smartmeter/ee3", payload=ee3)
            ee3_ = ee3

client.close()
