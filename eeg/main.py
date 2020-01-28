# coding:utf-8
import ble_device_scan
import mindwave

# mindwaveに接続
mindwave.EEG()

# M5StickCに接続
ble_device_scan.Peripheral()

# 値を継続的に取得する

# 脳波系の値が閾値を超えたら、M5StickCにWrite命令を送信

if __name__ == "__main__":
    PORT = '/dev/rfcomm1'
    MAC_ADDRESS = "D8:A0:1D:51:06:D2"
    BLE_HANGLE = 42

    m5Stickc = ble_device_scan.Peripheral(MAC_ADDRESS)

    mindwave_obj = ble_device_scan.EEG()
    shatter_flag = 0

    for packets in mindwave_obj.get_packets():
        for pkt in packets:
            if isinstance(pkt, tg.ThinkGearRawWaveData):
                continue

            if mindwave_obj.check_attention(str(pkt)) and shatter_flag == 0:
                print 'kacha'
                shatter_flag = 1
                # send write signal to m5stickc
                m5Stickc.write_characterristics(42, "test")
            else:
                shatter_flag = 0