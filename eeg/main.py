# coding:utf-8
import ble_device
from mindwave import is_attention, check_method
import thinkgear as tg


if __name__ == "__main__":
    PORT = '/dev/rfcomm1' # mindwaveの接続デバイス
    MAC_ADDRESS = "D8:A0:1D:51:06:D2" #m5stickcのmac address
    BLE_HANGLE = 42 # m5stickのBLEサービスハンドル

    m5Stickc = ble_device.Peripheral(MAC_ADDRESS)

    mindwave_obj = tg.ThinkGearProtocol(PORT)
    shatter_flag = 0

    for packets in mindwave_obj.get_packets():
        for pkt in packets:
            if isinstance(pkt, tg.ThinkGearRawWaveData):
                continue

            print get_attention_data(pkt)
            if is_attention(str(pkt)) and shatter_flag == 0:
                print 'Click!'
                shatter_flag = 1
                # send write signal to m5stickc
                m5Stickc.write_characterristics(42, "Click!")
            else:
                shatter_flag = 0
                m5Stickc.write_characterristics(42, get_attention_data(pkt))
