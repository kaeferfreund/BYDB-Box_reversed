from pymodbus.client.sync import ModbusSerialClient as ModbusClient

# http://www.logicio.com/HTML/ioext-modbuscommands.htm

client = ModbusClient(method='rtu', port='/dev/ptyp0', timeout=1, baudrate=9600)
client.connect()

if client.connect():
    rw = client.read_holding_registers(0x00, 0x00,  unit=0x00)

    print(result.bits[0])
    client.close()