# coding: utf-8
import re
import thinkgear as tg

PORT = '/dev/rfcomm1'

class EEG:
    def __init__(self):
        self.tg_device = tg.ThinkGearProtocol(PORT)
        self.AT_THRESHOLD = 80
    
    def get_packets(self):
        return self.tg_device.get_packets()
    
    def attention_data(self, pkt_t):
        if pkt_t != '' and "ATTENTION" in pkt_t:
            at_num = re.search(r'\d+', pkt_t)
            print at_num.group()
            return at_num.group()
        return 0

    def is_concentrate(self, attention_val):
        flag = False
        if self.AT_THRESHOLD <= int(attention_val):
            flag = True
        return flag

    def check_method(self):
        print type(self.tg_device)
        for x in dir(self.tg_device):
            print x
    
    def is_instance(self, pkt):
        if isinstance(pkt, tg.ThinkGearRawWaveData):
            return True
        else:
            return False


    def check_attention(self, pkt_t):
        attention_val = self.attention_data(pkt_t)
        return self.is_concentrate(attention_val)


if __name__ == "__main__":
    mindwave_obj = tg.ThinkGearProtocol(PORT)
    shatter_flag = 0

    for packets in mindwave_obj.get_packets():
        for pkt in packets:
            if isinstance(pkt, tg.ThinkGearRawWaveData):
                continue

            if check_attention(str(pkt)) and shatter_flag == 0:
                print 'kacha'
                shatter_flag = 1
                # ここで写真取る
            else:
                shatter_flag = 0
                