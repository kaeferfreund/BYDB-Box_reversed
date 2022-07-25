#!/usr/bin/env python

"""
Changed a lot of a Script originall created by Ralf Zimmermann (mail@ralfzimmermann.de) in 2020.
The orginal code and its documentation can be found on: https://github.com/RalfZim/venus.dbus-fronius-huawei
Used https://github.com/victronenergy/velib_python/blob/master/dbusdummyservice.py as basis for this service.
"""

"""
/data/Pathtothisscript/vedbus.py
/data/Pathtothisscript/ve_utils.py
python -m ensurepip --upgrade
pip install paho-mqtt
"""
try:
  from vedbus import VeDbusService
  import paho.mqtt.client as mqtt
  import os
  import json
  import sys
  import time
  import logging
  import platform
  import gobject  # Python 2.x
except:
  from gi.repository import GLib as gobject  # Python 3.x
try:
  import thread   # for daemon = True  / Python 2.x
except:
  import _thread as thread   # for daemon = True  / Python 3.x

# our own packages
sys.path.insert(1, os.path.join(
    os.path.dirname(__file__), '../ext/velib_python'))

path_UpdateIndex = '/UpdateIndex'

# MQTT Setup
broker_address = "192.168.21.23"
MQTTNAME = "victron_mqtt_huawei"

# Variblen setzen
verbunden = 0
active_power = 0
ac_v1 = 0
ac_v2 = 0
ac_v3 = 0
ac_c1 = 0
ac_c2 = 0
ac_c3 = 0
ac_p1 = 0
ac_p2 = 0
ac_p3 = 0
yield_total = 0

# MQTT Abfragen:

def on_disconnect(client, userdata, rc):
    global verbunden
    print("Client Got Disconnected")
    if rc != 0:
        print('Unexpected MQTT disconnection. Will auto-reconnect')

    else:
        print('rc value:' + str(rc))

    try:
        print("Trying to Reconnect")
        client.connect(broker_address)
        verbunden = 1
    except Exception as e:
        logging.exception("Fehler beim reconnecten mit Broker")
        print("Error in Retrying to Connect with Broker")
        verbunden = 0
        print(e)


def on_connect(client, userdata, flags, rc):
        global verbunden
        if rc == 0:
            print("Connected to MQTT Broker!")
            verbunden = 1
            client.subscribe("huawei/#")
        else:
            print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
    try:
        global active_power, ac_v1, ac_v2, ac_v3, ac_c1, ac_c2, ac_c3, yield_total, ac_p1, ac_p2, ac_p3
        
        if msg.topic == "huawei/active_power":
          active_power = float(msg.payload)
          
        if msg.topic == "huawei/ac_c1":
          ac_c1 = float(msg.payload)
          
        if msg.topic == "huawei/ac_c2":
          ac_c2 = float(msg.payload)
        
        if msg.topic == "huawei/ac_c3":
          ac_c3 = float(msg.payload)
        
        if msg.topic == "huawei/ac_v1":
          ac_v1 = float(msg.payload)
        
        if msg.topic == "huawei/ac_v2":
          ac_v2 = float(msg.payload)
          
        if msg.topic == "huawei/ac_v3":
          ac_v3 = float(msg.payload)
          
        if msg.topic == "huawei/ac_p1":
          ac_p1 = float(msg.payload)
        
        if msg.topic == "huawei/ac_p2":
          ac_p2 = float(msg.payload)
          
        if msg.topic == "huawei/ac_p3":
          ac_p3 = float(msg.payload)

        if msg.topic == "huawei/yield_total":
          yield_total = float(msg.payload)

    except Exception as e:
        logging.exception("Programm MQTTtoMeter ist abgestuerzt. (on message Funkion)")
        print(e)
        print("Im MQTTtoMeter Programm ist etwas beim auslesen der Nachrichten schief gegangen")




class DbusDummyService:
  def __init__(self, servicename, deviceinstance, paths, productname='Huawei SUN2000', connection='MQTT'):
    self._dbusservice = VeDbusService(servicename)
    self._paths = paths

    logging.debug("%s /DeviceInstance = %d" % (servicename, deviceinstance))

    # Create the management objects, as specified in the ccgx dbus-api document
    self._dbusservice.add_path('/Mgmt/ProcessName', __file__)
    self._dbusservice.add_path('/Mgmt/ProcessVersion', 'Unkown version, and running on Python ' + platform.python_version())
    self._dbusservice.add_path('/Mgmt/Connection', connection)

    # Create the mandatory objects
    self._dbusservice.add_path('/DeviceInstance', deviceinstance)
    self._dbusservice.add_path('/ProductId', 41284) 
    self._dbusservice.add_path('/ProductName', productname)
    self._dbusservice.add_path('/FirmwareVersion', 0.1)
    self._dbusservice.add_path('/HardwareVersion', 0)
    self._dbusservice.add_path('/Connected', 1)
    self._dbusservice.add_path('/ErrorCode', '(0) No Error')
    self._dbusservice.add_path('/Position', 0)

    for path, settings in self._paths.items():
      self._dbusservice.add_path(
        path, settings['initial'], writeable=True, onchangecallback=self._handlechangedvalue)

    gobject.timeout_add(100, self._update) # pause 1000ms before the next request
  
  def _update(self):
    self._dbusservice['/Ac/Power'] = active_power*1000.0

    self._dbusservice['/Ac/L1/Current'] = ac_c1
    self._dbusservice['/Ac/L2/Current'] = ac_c2
    self._dbusservice['/Ac/L3/Current'] = ac_c3
            
    self._dbusservice['/Ac/L1/Voltage'] = ac_v1
    self._dbusservice['/Ac/L2/Voltage'] = ac_v2
    self._dbusservice['/Ac/L3/Voltage'] = ac_v3
    
    self._dbusservice['/Ac/L1/Power'] = ac_p1
    self._dbusservice['/Ac/L2/Power'] = ac_p2
    self._dbusservice['/Ac/L3/Power'] = ac_p3

    self._dbusservice['/Ac/Energy/Forward'] = yield_total
    self._dbusservice['/Ac/Energy/Forward'] = yield_total
    self._dbusservice['/Ac/Energy/Forward'] = yield_total
    
    self._dbusservice['/Ac/L1/Energy/Forward'] = yield_total/3.0
    self._dbusservice['/Ac/L2/Energy/Forward'] = yield_total/3.0
    self._dbusservice['/Ac/L3/Energy/Forward'] = yield_total/3.0
    

    # increment UpdateIndex - to show that new data is available
    index = self._dbusservice[path_UpdateIndex] + 1  # increment index
    if index > 255:   # maximum value of the index
      index = 0       # overflow from 255 to 0
    self._dbusservice[path_UpdateIndex] = index
    return True

  def _handlechangedvalue(self, path, value):
    logging.debug("someone else updated %s to %s" % (path, value))
    return True # accept the change

def main():
  logging.basicConfig(level=logging.DEBUG) # use .INFO for less logging
  thread.daemon = True # allow the program to quit

  from dbus.mainloop.glib import DBusGMainLoop
  # Have a mainloop, so we can send/receive asynchronous calls to and from dbus
  DBusGMainLoop(set_as_default=True)
  
  pvac_output = DbusDummyService(
    servicename='com.victronenergy.pvinverter.pv0',
    deviceinstance=0,
    paths={
      '/Ac/Power': {'initial': 0},
      '/Ac/L1/Voltage': {'initial': 0},
      '/Ac/L2/Voltage': {'initial': 0},
      '/Ac/L3/Voltage': {'initial': 0},
      '/Ac/L1/Current': {'initial': 0},
      '/Ac/L2/Current': {'initial': 0},
      '/Ac/L3/Current': {'initial': 0},
      '/Ac/L1/Power': {'initial': 0},
      '/Ac/L2/Power': {'initial': 0},
      '/Ac/L3/Power': {'initial': 0},
      '/Ac/Energy/Forward': {'initial': 0},
      '/Ac/L1/Energy/Forward': {'initial': 0},
      '/Ac/L2/Energy/Forward': {'initial': 0},
      '/Ac/L3/Energy/Forward': {'initial': 0},
      path_UpdateIndex: {'initial': 0},
    })

  logging.info('Connected to dbus, and switching over to gobject.MainLoop() (= event based)')
  mainloop = gobject.MainLoop()
  mainloop.run()

# Konfiguration MQTT
client = mqtt.Client(MQTTNAME) # create new instance
client.on_disconnect = on_disconnect
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address)  # connect to broker

client.loop_start()

if __name__ == "__main__":
  main()