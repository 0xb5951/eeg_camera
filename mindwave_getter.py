import re
import thinkgear as tg

PORT = '/dev/rfcomm1'
AT_THRESHOLD = 20

def check_method(terget):
    print type(terget)
    for x in dir(terget):
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
    # check_method(thinkgear)
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
                