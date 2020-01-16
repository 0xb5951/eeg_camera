#include <M5StickC.h>
#include "BLEDevice.h"

// 検索するBLEデバイス。serviceUUIDを調べる場合には空にする(例はHuman Interface Device"00001812-0000-1000-8000-00805f9b34fb")
static BLEUUID serviceUUID("");
static BLEAddress *deviceMacAddres;

static BLEAdvertisedDevice *myDevice;
BLEScan *pBLEScan;

// 接続してCharacteristic一覧を取得
bool searchBleDevice() {

    Serial.print("接続先 : ");
    Serial.println(myDevice->getAddress().toString().c_str());
    BLEClient *pClient = BLEDevice::createClient();
    pClient->connect(myDevice);

    // サービス取得
    BLERemoteService *pRemoteService = pClient->getService(serviceUUID);
    if (pRemoteService == nullptr)
    {
        pClient->disconnect();
        return false;
    }

    // Characteristic一覧
    Serial.println("characteristic一覧");
    std::map<std::string, BLERemoteCharacteristic *> *mapCharacteristics = pRemoteService->getCharacteristics();
    for (std::map<std::string, BLERemoteCharacteristic *>::iterator i = mapCharacteristics->begin(); i != mapCharacteristics->end(); ++i)
    {
        Serial.print(" - characteristic UUID : ");
        Serial.print(i->first.c_str());
        Serial.print(" Broadcast:");
        Serial.print(i->second->canBroadcast() ? 'O' : 'X');
        Serial.print(" Read:");
        Serial.print(i->second->canRead() ? 'O' : 'X');
        Serial.print(" WriteNoResponse:");
        Serial.print(i->second->canWriteNoResponse() ? 'O' : 'X');
        Serial.print(" Write:");
        Serial.print(i->second->canWrite() ? 'O' : 'X');
        Serial.print(" Notify:");
        Serial.print(i->second->canNotify() ? 'O' : 'X');
        Serial.print(" Indicate:");
        Serial.print(i->second->canIndicate() ? 'O' : 'X');
        Serial.println();
    }

    // stop
    Serial.println("プログラム停止!");
    while (1)
        delay(1000);
}

// マニュファクチャラーデータを元にBLEデバイスに接続する
void connectBleDevice()
{
    BLEScanResults foundDevices = pBLEScan->start(3); //スキャンを開始
    int count = foundDevices.getCount();              // スキャンで見つけたデバイス数を取得

    for (int i = 0; i < count; i++)
    {
        BLEAdvertisedDevice d = foundDevices.getDevice(i); // デバイスの情報をそれぞれ取得
        if (d.haveManufacturerData())
        {                                               // マニュファクチャラデータを持っていれば
            std::string data = d.getManufacturerData(); // マニュファクチャラデータを取得
            int manu = data[1] << 8 | data[0];
            Serial.println(manu);
        }
    }
}

// 検索したデバイスを受信するコールバック関数
class MyAdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks
{
    void onResult(BLEAdvertisedDevice advertisedDevice)
    {
        Serial.print("BLE デバイス発見 : ");
        Serial.println(advertisedDevice.toString().c_str());
        Serial.println(advertisedDevice.getManufacturerData().c_str());

        if (advertisedDevice.haveServiceUUID() && advertisedDevice.isAdvertisingService(serviceUUID))
        {
            // 指定デバイスだったら接続する
            BLEDevice::getScan()->stop();
            myDevice = new BLEAdvertisedDevice(advertisedDevice);
        }
    }
};

void setup()
{
    // Initialize the M5StickC object
    M5.begin();
    // 6軸センサ初期化
    M5.MPU6886.Init();
    M5.Lcd.setRotation(1); // ボタンBが上になる向き
    M5.Lcd.fillScreen(BLACK);

    Serial.begin(115200);
    Serial.println("BLEデバイス検索開始...");

    // デバイスの初期化
    BLEDevice::init("");
    pBLEScan = BLEDevice::getScan(); // スキャンオブジェクトを取得
    pBLEScan->setActiveScan(false);  // パッシブスキャンを設定
    pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
    pBLEScan->setInterval(1349);
    pBLEScan->setWindow(449);
    pBLEScan->start(5, false);
}

void loop()
{
    // if (myDevice != NULL)
    // {
    // searchBleDevice();
    // }
    M5.Lcd.printf("Loop process");
    delay(1000);
}