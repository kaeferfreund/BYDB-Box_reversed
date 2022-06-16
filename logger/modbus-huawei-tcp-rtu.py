#!/usr/bin/python
from lib2to3.pytree import convert
import sys
import ctypes
from time import sleep
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer
import numpy as np
from collections import OrderedDict
import paho.mqtt.client as mqtt


client = ModbusClient("192.168.21.150", port=502, framer=ModbusRtuFramer)
mqtt_client =mqtt.Client("huawei")
mqtt_client.connect("192.168.21.23", port=1883, keepalive=60, bind_address="")

for x in range(20000):
    
    #if hasattr(response, "registers"):
        
    response = client.read_holding_registers(address=32114, count=2, unit=1)
    yield_today = np.left_shift(np.int32(response.registers[0]),16) | np.int32(response.registers[1])
    mqtt_client.publish("huawei/yield_today", payload=float(yield_today)/100.0)
        
    response = client.read_holding_registers(address=32106, count=2, unit=1)
    yield_total = np.left_shift(np.int32(response.registers[0]),16) | np.int32(response.registers[1])
    mqtt_client.publish("huawei/yield_total", payload=float(yield_total)/100.0)
        
    response = client.read_holding_registers(address=32078, count=2, unit=1)
    today_peak_power = np.int32(np.left_shift(np.int16(response.registers[0]),16) | np.int32(response.registers[1]))
    mqtt_client.publish("huawei/today_peak_power", payload=float(today_peak_power)/1000.0)
    
    response = client.read_holding_registers(address=32080, count=2, unit=1)
    active_power = np.int32(np.left_shift(np.int16(response.registers[0]),16) | np.int32(response.registers[1]))
    mqtt_client.publish("huawei/active_power", payload=float(active_power)/1000.0)

    response = client.read_holding_registers(address=32072, count=2, unit=1)
    ac_c1 = float(np.int32(np.left_shift(np.int16(response.registers[0]),16) | np.int32(response.registers[1])))/1000.0
    mqtt_client.publish("huawei/ac_c1", payload=ac_c1)
    
    response = client.read_holding_registers(address=32074, count=2, unit=1)
    ac_c2 = float(np.int32(np.left_shift(np.int16(response.registers[0]),16) | np.int32(response.registers[1])))/1000.0
    mqtt_client.publish("huawei/ac_c2", payload=ac_c2)
    
    response = client.read_holding_registers(address=32076, count=2, unit=1)
    ac_c3 = float(np.int32(np.left_shift(np.int16(response.registers[0]),16) | np.int32(response.registers[1])))/1000.0
    mqtt_client.publish("huawei/ac_c3", payload=ac_c3)
    
    response = client.read_holding_registers(address=32016, count=1, unit=1)
    pv_v1 = np.int16(response.registers[0])
    mqtt_client.publish("huawei/pv_v1", payload=float(pv_v1)/10.0)
    
    response = client.read_holding_registers(address=32018, count=1, unit=1)
    pv_v2 = np.int16(response.registers[0])
    mqtt_client.publish("huawei/pv_v2", payload=float(pv_v2)/10.0)
    
    response = client.read_holding_registers(address=32020, count=1, unit=1)
    pv_v3 = np.int16(response.registers[0])
    mqtt_client.publish("huawei/pv_v3", payload=float(pv_v3)/10.0)
    
    response = client.read_holding_registers(address=32022, count=1, unit=1)
    pv_v4 = np.int16(response.registers[0])
    mqtt_client.publish("huawei/pv_v4", payload=float(pv_v4)/10.0)
    
    response = client.read_holding_registers(address=32017, count=1, unit=1)
    pv_c1 = float(np.int16(response.registers[0]))/100.0
    mqtt_client.publish("huawei/pv_c1", payload=pv_c1)
    
    response = client.read_holding_registers(address=32019, count=1, unit=1)
    pv_c2 = float(np.int16(response.registers[0]))/100.0
    mqtt_client.publish("huawei/pv_c2", payload=pv_c2)
    
    response = client.read_holding_registers(address=32021, count=1, unit=1)
    pv_c3 = float(np.int16(response.registers[0]))/100.0
    mqtt_client.publish("huawei/pv_c3", payload=pv_c3)
    
    response = client.read_holding_registers(address=32023, count=1, unit=1)
    pv_c4 = np.int16(response.registers[0])
    mqtt_client.publish("huawei/pv_c4", payload=float(pv_c4)/100.0)
    
    mqtt_client.publish("huawei/pv_p1", payload=(float(pv_c1)/100.0*float(pv_v1)/10.0/1000.0))
    mqtt_client.publish("huawei/pv_p2", payload=(float(pv_c2)/100.0*float(pv_v2)/10.0/1000.0))
    mqtt_client.publish("huawei/pv_p3", payload=(float(pv_c3)/100.0*float(pv_v3)/10.0/1000.0))
    mqtt_client.publish("huawei/pv_p4", payload=(float(pv_c4)/100.0*float(pv_v4)/10.0/1000.0))
      
    response = client.read_holding_registers(address=32069, count=1, unit=1)
    ac_v1 = float(np.int16(response.registers[0]))/10.0
    mqtt_client.publish("huawei/ac_v1", payload=ac_v1)
    
    response = client.read_holding_registers(address=32070, count=1, unit=1)
    ac_v2 = float(np.int16(response.registers[0]))/10.0
    mqtt_client.publish("huawei/ac_v2", payload=ac_v2)
    
    response = client.read_holding_registers(address=32071, count=1, unit=1)
    ac_v3 = float(np.int16(response.registers[0]))/10.0
    mqtt_client.publish("huawei/ac_v3", payload=ac_v3)
    
    response = client.read_holding_registers(address=32084, count=1, unit=1)
    pf = float(np.int16(response.registers[0]))/1000.0
    mqtt_client.publish("huawei/pf", payload=pf)
    
    response = client.read_holding_registers(address=40122, count=1, unit=1)
    pf2 = float(np.int16(response.registers[0]))/1000.0
    mqtt_client.publish("huawei/pf2", payload=pf)
    
    mqtt_client.publish("huawei/ac_p1", payload=(ac_v1*ac_c1*pf))
    mqtt_client.publish("huawei/ac_p2", payload=(ac_v2*ac_c2*pf))
    mqtt_client.publish("huawei/ac_p3", payload=(ac_v3*ac_c3*pf))

client.close()