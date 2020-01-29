# coding:utf-8
import ble_device
import mindwave

if __name__ == "__main__":
    PORT = '/dev/rfcomm1' # mindwaveの接続デバイス
    MAC_ADDRESS = "D8:A0:1D:51:06:D2" #m5stickcのmac address
    BLE_HANGLE = 42 # m5stickのBLEサービスハンドル

    m5Stickc = ble_device.Peripheral(MAC_ADDRESS)

    mindwave_obj = mindwave.EEG()
    shatter_flag = 0

    for packets in mindwave_obj.get_packets():
        for pkt in packets:
            if mindwave_obj.is_instance(pkt):
                continue
            if mindwave_obj.check_attention(str(pkt)) and shatter_flag == 0:
                print 'kacha'
                shatter_flag = 1
                # send write signal to m5stickc
                m5Stickc.write_characterristics(42, "kacha")
            else:
                shatter_flag = 0