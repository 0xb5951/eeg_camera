#include <M5StickC.h>
#include "BLEDevice.h"
 
// 検索するBLEデバイス。serviceUUIDを調べる場合には空にする(例はHuman Interface Device"00001812-0000-1000-8000-00805f9b34fb")
static BLEUUID serviceUUID();
 
static BLEAdvertisedDevice* myDevice;
 
// 接続してCharacteristic一覧を取得
bool connectToServer() {
  Serial.print("接続先 : ");
  Serial.println(myDevice->getAddress().toString().c_str());
  BLEClient*  pClient  = BLEDevice::createClient();
  pClient->connect(myDevice);
 
  // サービス取得
  BLERemoteService* pRemoteService = pClient->getService(serviceUUID);
  if (pRemoteService == nullptr) {
    pClient->disconnect();
    return false;
  }
 
  // Characteristic一覧
  Serial.println("characteristic一覧");
  std::map<std::string, BLERemoteCharacteristic*>* mapCharacteristics = pRemoteService->getCharacteristics();
  for (std::map<std::string, BLERemoteCharacteristic*>::iterator i = mapCharacteristics->begin(); i != mapCharacteristics->end(); ++i) {
    Serial.print(" - characteristic UUID : ");
    Serial.print(i->first.c_str());
    Serial.print(" Broadcast:");
    Serial.print(i->second->canBroadcast()?'O':'X');
    Serial.print(" Read:");
    Serial.print(i->second->canRead()?'O':'X');
    Serial.print(" WriteNoResponse:");
    Serial.print(i->second->canWriteNoResponse()?'O':'X');
    Serial.print(" Write:");
    Serial.print(i->second->canWrite()?'O':'X');
    Serial.print(" Notify:");
    Serial.print(i->second->canNotify()?'O':'X');
    Serial.print(" Indicate:");
    Serial.print(i->second->canIndicate()?'O':'X');
    Serial.println();
  }
 
  // stop
  Serial.println("プログラム停止!");
  while (1) delay(1000);
}
 
// 検索したデバイスを受信するコールバック関数
class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
    void onResult(BLEAdvertisedDevice advertisedDevice) {
      Serial.print("BLE デバイス発見 : ");
      Serial.println(advertisedDevice.toString().c_str());
 
      if (advertisedDevice.haveServiceUUID() && advertisedDevice.isAdvertisingService(serviceUUID)) {
        // 指定デバイスだったら接続する
        BLEDevice::getScan()->stop();
        myDevice = new BLEAdvertisedDevice(advertisedDevice);
      }
    }
};
 
void setup() {
  Serial.begin(115200);
  Serial.println("BLEデバイス検索開始...");
  BLEDevice::init("");
 
  BLEScan* pBLEScan = BLEDevice::getScan();
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setInterval(1349);
  pBLEScan->setWindow(449);
  pBLEScan->setActiveScan(true);
  pBLEScan->start(5, false);
}
 
void loop() {
  if (myDevice != NULL) {
    connectToServer();
  }
 
  delay(1000);
}