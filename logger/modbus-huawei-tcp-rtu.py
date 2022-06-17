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

yield_today_=yield_total_=today_peak_power_=active_power_=0
ac_c1_=ac_c2_=ac_c3_=0
pv_v1_=pv_v2_=pv_v3_=pv_v4_=0
pv_c1_=pv_c2_=pv_c3_=pv_c4_=0
p1_=p2_=p3_=p4_=0
ac_p1_=ac_p2_=ac_p3_=0
ac_v1_=ac_v2_=ac_v3_=0
pf_=pf2_=0

for x in range(20000):
    
    #if hasattr(response, "registers"):
        
    response = client.read_holding_registers(address=32114, count=2, unit=1)
    yield_today = np.left_shift(np.int32(response.registers[0]),16) | np.int32(response.registers[1])/100.0
    if(yield_today != yield_today_):
        mqtt_client.publish("huawei/yield_today", payload=yield_today)
        
    response = client.read_holding_registers(address=32106, count=2, unit=1)
    yield_total = np.left_shift(np.int32(response.registers[0]),16) | np.int32(response.registers[1])/100.0
    if(p1 != p1_):
        mqtt_client.publish("huawei/yield_total", payload=yield_total
        
    response = client.read_holding_registers(address=32078, count=2, unit=1)
    today_peak_power = np.int32(np.left_shift(np.int16(response.registers[0]),16) | np.int32(response.registers[1]))/1000.0
    if(today_peak_power != today_peak_power_):
        mqtt_client.publish("huawei/today_peak_power", payload=today_peak_power
    
    response = client.read_holding_registers(address=32080, count=2, unit=1)
    active_power = np.int32(np.left_shift(np.int16(response.registers[0]),16) | np.int32(response.registers[1]))
    if(active_power != active_power_):
        mqtt_client.publish("huawei/active_power", payload=float(active_power)/1000.0)

    response = client.read_holding_registers(address=32072, count=2, unit=1)
    ac_c1 = float(np.int32(np.left_shift(np.int16(response.registers[0]),16) | np.int32(response.registers[1])))/1000.0
    if(ac_c1 != ac_c1_):
        mqtt_client.publish("huawei/ac_c1", payload=ac_c1)
    
    response = client.read_holding_registers(address=32074, count=2, unit=1)
    ac_c2 = float(np.int32(np.left_shift(np.int16(response.registers[0]),16) | np.int32(response.registers[1])))/1000.0
    if(ac_c2 != ac_c2_):
        mqtt_client.publish("huawei/ac_c2", payload=ac_c2)
    
    response = client.read_holding_registers(address=32076, count=2, unit=1)
    ac_c3 = float(np.int32(np.left_shift(np.int16(response.registers[0]),16) | np.int32(response.registers[1])))/1000.0
    if(ac_c3 != ac_c3_):
        mqtt_client.publish("huawei/ac_c3", payload=ac_c3)
    
    response = client.read_holding_registers(address=32016, count=1, unit=1)
    pv_v1 = np.int16(response.registers[0])/10.0
    if(pv_v1 != pv_v1_):
        mqtt_client.publish("huawei/pv_v1", payload=pv_v1)
    
    response = client.read_holding_registers(address=32018, count=1, unit=1)
    pv_v2 = np.int16(response.registers[0])/10.0
    if(pv_v2 != pv_v2_):
        mqtt_client.publish("huawei/pv_v2", payload=pv_v2)
    
    response = client.read_holding_registers(address=32020, count=1, unit=1)
    pv_v3 = np.int16(response.registers[0])/10.0
    if(pv_v3 != pv_v3_):
        mqtt_client.publish("huawei/pv_v3", payload=pv_v3)
    
    response = client.read_holding_registers(address=32022, count=1, unit=1)
    pv_v4 = np.int16(response.registers[0])/10.0
    if(pv_v4 != pv_v4_):
        mqtt_client.publish("huawei/pv_v4", payload=pv_v4)
                        
    response = client.read_holding_registers(address=32017, count=1, unit=1)
    pv_c1 = float(np.int16(response.registers[0]))/100.0
    if(pv_c1 != pv_c1_):
        mqtt_client.publish("huawei/pv_c1", payload=pv_c1)
    
    response = client.read_holding_registers(address=32019, count=1, unit=1)
    pv_c2 = float(np.int16(response.registers[0]))/100.0
    if(pv_c2 != pv_c2_):
        mqtt_client.publish("huawei/pv_c2", payload=pv_c2)
    
    response = client.read_holding_registers(address=32021, count=1, unit=1)
    pv_c3 = float(np.int16(response.registers[0]))/100.0
    if(pv_c3 != pv_c3_):    
        mqtt_client.publish("huawei/pv_c3", payload=pv_c3)
    
    response = client.read_holding_registers(address=32023, count=1, unit=1)
    pv_c4 = np.int16(response.registers[0])/100.0
    if(pv_c4 != pv_c4_):
        mqtt_client.publish("huawei/pv_c4", payload=pv_c4)
    
    p1= pv_c1*pv_v1
    p2= pv_c2*pv_v2
    p3= pv_c3*pv_v3
    p4= pv_c4*pv_v4
    
    if(p1 != p1_):
        mqtt_client.publish("huawei/pv_p1", payload=p1)
    if(p2 != p2_):
        mqtt_client.publish("huawei/pv_p2", payload=p2)
    if(p3 != p3_):
        mqtt_client.publish("huawei/pv_p3", payload=p3)
    if(p4 != p4_):
        mqtt_client.publish("huawei/pv_p4", payload=p4)
      
    response = client.read_holding_registers(address=32069, count=1, unit=1)
    ac_v1 = float(np.int16(response.registers[0]))/10.0
    if(ac_v1 != ac_v1_):
        mqtt_client.publish("huawei/ac_v1", payload=ac_v1)
    
    response = client.read_holding_registers(address=32070, count=1, unit=1)
    ac_v2 = float(np.int16(response.registers[0]))/10.0
    if(ac_v2 != ac_v2_):
        mqtt_client.publish("huawei/ac_v2", payload=ac_v2)
    
    response = client.read_holding_registers(address=32071, count=1, unit=1)
    ac_v3 = float(np.int16(response.registers[0]))/10.0
    if(ac_v3 != ac_v3_):
        mqtt_client.publish("huawei/ac_v3", payload=ac_v3)
    
    response = client.read_holding_registers(address=32084, count=1, unit=1)
    pf = float(np.int16(response.registers[0]))/1000.0
    if(pf != pf_):
        mqtt_client.publish("huawei/pf", payload=pf)
    
    response = client.read_holding_registers(address=40122, count=1, unit=1)
    pf2 = float(np.int16(response.registers[0]))/1000.0
    if(pf2 != pf2_):
        mqtt_client.publish("huawei/pf2", payload=pf2)
    
    ac_p1 = ac_v1*ac_c1*pf
    ac_p2 = ac_v2*ac_c2*pf
    ac_p3 = ac_v3*ac_c3*pf
    
    if(ac_p1 != ac_p1_):
        mqtt_client.publish("huawei/ac_p1", payload=ac_p1)
    if(ac_p2 != ac_p2_):
        mqtt_client.publish("huawei/ac_p2", payload=ac_p2)
    if(ac_p3 != ac_p3_):
        mqtt_client.publish("huawei/ac_p3", payload=ac_p3)

client.close()