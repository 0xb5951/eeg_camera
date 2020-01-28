# coding: utf-8
import re
import thinkgear as tg

PORT = '/dev/rfcomm1'

class EEG:
    def __init__(self, PORT):
        self.tg_device = tg.ThinkGearProtocol(PORT)
        self.AT_THRESHOLD = 90
    
    def get_packets(self):
        return self.tg_device.get_packets()
    
    def attention_data(self, pkt_t: str):
        if pkt_t != '' and "ATTENTION" in pkt_t:
            at_num = re.search(r'\d+', pkt_t)
            return at_num.group()
    
    def is_concentrate(self, attention_val: int):
        flag = False
        if self.AT_THRESHOLD >= int(attention_val):
            flag = True
        return flag

    def check_method(self):
        print type(self.tg_device)
        for x in dir(self.tg_device):
            print x


def check_attention(pkt_t):
    flag = False
    if pkt_t != '' and "ATTENTION" in pkt_t:
        at_num = re.search(r'\d+', pkt_t)
        print at_num.group()
        if AT_THRESHOLD >= int(at_num.group()):
            flag = True
            
    return flag


if __name__ == "__main__":
    mindwave_obj = EEG(PORT)
    shatter_flag = 0

    for packets in mindwave_obj.get_packets():
        for pkt in packets:
            if isinstance(pkt, tg.ThinkGearRawWaveData):
                continue

            if mindwave_obj.check_attention(str(pkt)) and shatter_flag == 0:
                print 'kacha'
                shatter_flag = 1
                # ここで写真取る
            else:
                shatter_flag = 0
                