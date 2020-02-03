#include <M5StickC.h>
#include <WiFi.h>
#include <ArduinoJson.h>
#include <ssl_client.h>
#include <WiFiClientSecure.h>

// デバイス初期化
// BLEserverを作成
// wifiに接続
// write命令を受け取る
// M5StickVに受信信号を送る
// M5StickVから画像情報を受け取る
// slackとかに送信

HardwareSerial serial_ext(2);

typedef struct {
  uint32_t length;
  uint8_t *buf;
} jpeg_data_t;

jpeg_data_t jpeg_data;
static const int RX_BUF_SIZE = 20000;
static const uint8_t packet_begin[3] = { 0xFF, 0xD8, 0xEA };
   
void get_image_data()
{
    if (serial_ext.available()) {
    uint8_t rx_buffer[10];
    int rx_size = serial_ext.readBytes(rx_buffer, 10);
    if (rx_size == 10) {
      // スタートパケットが一致したら

      if ((rx_buffer[0] == packet_begin[0]) && (rx_buffer[1] == packet_begin[1]) && (rx_buffer[2] == packet_begin[2])) {
        //image size receive of packet_begin
        jpeg_data.length = (uint32_t)(rx_buffer[4] << 16) | (rx_buffer[5] << 8) | rx_buffer[6];
        int rx_size = serial_ext.readBytes(jpeg_data.buf, jpeg_data.length);
        // 画像の中身 : jpeg_data.buf
        // 画像のサイズ : jpeg_data.length

        send_slack(jpeg_data.buf, jpeg_data.length);
        Serial.println("Captured!!");
      }
    }
  }
  // ちょっとロックをかける
  vTaskDelay(10 / portTICK_RATE_MS);
}

void setup() {
  // Initialize the M5StickC object
  M5.begin();
  // 6軸センサ初期化
  M5.MPU6886.Init();
  M5.Lcd.setRotation(1);  // ボタンBが上になる向き
  M5.Lcd.fillScreen(BLACK);

  wifi_setup();
  create_BLE_server();

  jpeg_data.buf = (uint8_t *) malloc(sizeof(uint8_t) * RX_BUF_SIZE);
  jpeg_data.length = 0;
  if (jpeg_data.buf == NULL) {
    Serial.println("malloc jpeg buffer 1 error");
  }

  serial_ext.begin(115200, SERIAL_8N1, 32, 33);
  M5.Lcd.fillScreen(BLACK);
  M5.Lcd.setTextSize(2.5);
}

void loop() {
  M5.update();
  get_image_data();
}