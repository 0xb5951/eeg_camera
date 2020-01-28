# coding: utf-8
from bluepy import btle

class Peripheral:
    def __init__(self, MAC_ADDRESS):
        self.peripheral = btle.Peripheral(MAC_ADDRESS)
    
    def write_characterristics(self, handle, text):
        return self.peripheral.writeCharacteristic(handle, text, True)

    def get_device_data(self):
        for service in self.peripheral.getServices():
            print("serviceUUID: " + str(service.uuid))
            for characteristic in service.getCharacteristics():
                print("characteristicUUID: " + str(characteristic.uuid))
                print("handle: " + str(characteristic.getHandle()))
                print("property: " + characteristic.propertiesToString())

    def read_characterristics(self, pointer):
        data = self.peripheral.readCharacteristic(pointer)
        print(str(pointer) + ":")
        print(type(data))
        print(data)

if __name__ == "__main__":
    MAC_ADDRESS = "D8:A0:1D:51:06:D2"
    device = Peripheral(MAC_ADDRESS)
    print('start:')
    device.get_device_data()
    for i in range(42, 43):
        device.read_characterristics(i)

    device.write_characterristics(42, "test")
