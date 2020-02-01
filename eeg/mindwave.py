# coding: utf-8
import re
import thinkgear as tg

PORT = '/dev/rfcomm1'
AT_THRESHOLD = 80

def check_method():
    print type(tg_device)
    for x in dir(tg_device):
        print x

def is_attention(pkt_t):
    flag = False
    if AT_THRESHOLD <= int(get_attention_data(pkt_t)):
        flag = True
    return flag

def get_attention_data(pkt_t):
    if pkt_t != '' and "ATTENTION" in pkt_t:
        at_num = re.search(r'\d+', pkt_t)
        return at_num.group()
    return 0

if __name__ == "__main__":
    mindwave_obj = tg.ThinkGearProtocol(PORT)
    shatter_flag = 0

    for packets in mindwave_obj.get_packets():
        for pkt in packets:
            if isinstance(pkt, tg.ThinkGearRawWaveData):
                continue

            print(get_attention_data(str(pkt)))
            if is_attention(str(pkt)) and shatter_flag == 0:
                print 'kacha'
                shatter_flag = 1
                # ここで写真取る
            else:
                shatter_flag = 0
                