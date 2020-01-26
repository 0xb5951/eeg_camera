#include <M5StickC.h>
#include "BLEDevice.h"

static BLEUUID ServiceUUID("012bfff1-2c92-11e3-9e06-0002a5d5c413");
static BLEUUID CharacteristicUUID("012bfff4-2c92-11e3-9e06-0002a5d5c413");

class MyCallbackHandler: public BLECharacteristicCallbacks {
  void onRead(BLECharacteristic *pCharacteristic) {
    M5.Lcd.println("read");
    pCharacteristic->setValue("Hello World!");
  }

  void onWrite(BLECharacteristic *pCharacteristic) {
    M5.Lcd.println("write");
    std::string value = pCharacteristic->getValue();
    M5.Lcd.println(value.c_str());
  }
}

void setup()
{
    // Initialize the BLE environment
    BLEDevice::init("M5StickC");

    // Create the server
    BLEServer *pServer = BLEDevice::createServer();

    // Create the service
    BLEService *pService = pServer->createService(ServiceUUID);

    // Create the characteristic
    BLECharacteristic *pCharacteristic = pService->createCharacteristic(CharacteristicUUID, (uint32_t)'0x0011');

    // setCallbacks
    pCharacteristic->setCallbacks(new MyCallbackHandler());

    // Set the characteristic value
    pCharacteristic->setValue("Hello world");

    // Start the service
    pService->start();
    
    // start Advertising
    BLEAdvertising *pAdvertising = pServer->getAdvertising();
    pAdvertising->start();
}

void loop()
{
    //   if (Serial.available()) {
    //     SerialBT.write(Serial.read());
    //   }
    //   if (SerialBT.available()) {
    //     Serial.write(SerialBT.read());
    //   }
    delay(1000);
}
