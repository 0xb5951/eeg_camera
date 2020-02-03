#include <M5StickC.h>
#include "BLEDevice.h"
#define TFT_RED         0xF800      /* 255,   0,   0 */

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
    // ここで写真取る命令をM5StickVに送る
    Serial.println("write");
    std::string value = pCharacteristic->getValue();
    M5.Lcd.setTextSize(3);
    M5.Lcd.setCursor(65, 45);
    M5.Lcd.printf(value.c_str());
    if (strcmp(value.c_str(), "Click!") == 0) {
      M5.Lcd.fillScreen(WHITE);
      serial_ext.write(value.c_str()); // stickVに送信
      delay(50);
      M5.Lcd.fillScreen(BLACK);
      M5.Lcd.setTextSize(2);
      M5.Lcd.setCursor(2, 2);
      M5.Lcd.printf("Attention Num");
      M5.Lcd.setTextSize(1.5);
      M5.Lcd.setCursor(40, 22);
      M5.Lcd.printf("Threshold : 80");
    }
  }
};

void create_BLE_server() {
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
