# coding: utf-8
import re
import thinkgear as tg

# 脳波を読み取って特定条件でフラグを返すクラス

PORT = '/dev/rfcomm1'
AT_THRESHOLD = 20

class mindwave_wrapper(object):
    def __init__(self):
        self.tgp = tg.ThinkGearProtocol(PORT)

    def get_packets(self):
        return mindwave_obj.get_packets()
        

    def check_attribute(self):
        for attribute in dir(self.tgp):
            print attribute
    
    def check_attention(self, pkt_t):
        if pkt_t != '' and "ATTENTION" in pkt_t:
            at_num = re.search(r'\d+', pkt_t)
            return int(at_num.group())

    def is_concentrate(self):
    

            if AT_THRESHOLD >= int(at_num.group()):
                flag = True
                
        return flag


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
                