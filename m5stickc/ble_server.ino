#include <M5StickC.h>
#include "BLEDevice.h"

// 自由に設定してよい。以下でランダムなUUIDを生成してくれる。
// https://www.uuidgenerator.net
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
};

def create_BLE_server() {
    BLEDevice::init("M5StickC"); // Initialize the BLE environment

    // create GATT
    BLEServer *pServer = BLEDevice::createServer();
    BLEService *pService = pServer->createService(ServiceUUID);
    BLECharacteristic *pCharacteristic = pService->createCharacteristic(CharacteristicUUID, (uint32_t)'0x0011');

    // setCallback function
    pCharacteristic->setCallbacks(new MyCallbackHandler());

    // Start the service
    pService->start();
    
    // start Advertising
    BLEAdvertising *pAdvertising = pServer->getAdvertising();
    pAdvertising->start();

}

void setup()
{
    // Initialize the M5StickC object
    M5.begin();
    M5.Lcd.fillScreen(BLACK);
    Serial.begin(57600);
    create_BLE_server();
}

void loop()
{
    delay(1000);
}
