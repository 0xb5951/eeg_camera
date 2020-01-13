import re
import thinkgear as tg

PORT = '/dev/rfcomm1'
AT_THRESHOLD = 20

def check_method(terget):
    print type(terget)
    for x in dir(terget):
        print x


def check_attention(pkt_t):
    if pkt_t != '' and "ATTENTION" in pkt_t:
        at_num = re.search(r'\d+', pkt_t)
        print at_num.group()
        if AT_THRESHOLD >= int(at_num.group()):
            print 'kacha'

if __name__ == "__main__":
    # check_method(thinkgear)
    mindwave_obj = tg.ThinkGearProtocol(PORT)

    for packets in mindwave_obj.get_packets():
        for pkt in packets:
            if isinstance(pkt, tg.ThinkGearRawWaveData):
                continue

            check_attention(str(pkt))
