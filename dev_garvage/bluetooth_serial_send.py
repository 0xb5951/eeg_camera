import bluetooth
from time import sleep

mac_address = "D8:A0:1D:51:06:D2"
central_name = "central"
connect_port = 1

ble_server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
while(1):
    try:
        print mac_address + " : Connect......"
        ble_server.connect((mac_address, connect_port))
        sleep(2)
        print mac_address + " : Successful Connected!!!"
        break
    except bluetooth.BluetoothError:
        print mac_address + " : connecting failed"
        print "try connecting"
        sleep(1)
    except KeyboardInterrupt:
        break

while 1:
    try:
        ble_server.send("Hello World")
        print "data send"
        sleep(1)
    except KeyboardInterrupt:
        print 
