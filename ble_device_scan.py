# coding: utf-8
from bluepy import btle

MAC_ADDRESS = "D8:A0:1D:51:06:D2"

peripheral = btle.Peripheral(MAC_ADDRESS)


def get_device_data():
    for service in peripheral.getServices():
        print("serviceUUID: " + str(service.uuid))
        for characteristic in service.getCharacteristics():
            print("characteristicUUID: " + str(characteristic.uuid))
            print("handle: " + str(characteristic.getHandle()))
            print("property: " + characteristic.propertiesToString())


def read_characterristics(pointer):
    data = peripheral.readCharacteristic(pointer)
    # datas = peripheral.getCharacteristics(27,28)
    print(str(pointer) + ":")
    print(type(data))
    print(data)


if __name__ == "__main__":
    print('start:')
    get_device_data()
    for i in range(42, 43):
        read_characterristics(i)  
