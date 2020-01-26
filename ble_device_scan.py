# coding: utf-8  
from bluepy import btle

MAC_ADDRESS = "00:81:F9:29:AE:44"

peripheral = btle.Peripheral(MAC_ADDRESS)

for service in peripheral.getServices():
    print("serviceUUID: " + str(service.uuid))
    for characteristic in service.getCharacteristics():
        print("characteristicUUID: " + str(characteristic.uuid))
        print("handle: " + str(characteristic.getHandle()))
        print("property: " + characteristic.propertiesToString())
