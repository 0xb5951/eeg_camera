# coding: utf-8  
from bluepy import btle

MAC_ADDRESS = "00:81:F9:29:AE:44"

peripheral = btle.Peripheral(MAC_ADDRESS)

for service in peripheral.getServices():
    print("UUID：{service.uuid}")
    for characteristic in service.getCharacteristics():
        print('UUID：{characteristic.uuid}')
        print('ハンドル：{characteristic.getHandle()}')
        print('プロパティ：{characteristic.propertiesToString()}')
