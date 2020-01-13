import re
import thinkgear as tg

PORT = '/dev/rfcomm1'

def check_method(terget):
    print type(terget)
    for x in dir(terget):
        print x

if __name__ == "__main__":
    # check_method(thinkgear)
    mindwave_obj = tg.ThinkGearProtocol(PORT)

    for packets in mindwave_obj.get_packets():
        for pkt in packets:
            if isinstance(pkt, tg.ThinkGearRawWaveData):
                continue

            pkt_t = str(pkt)
            if pkt_t != '' and "ATTENTION" in pkt_t:
                    at_num = re.search(r'\d+', pkt_t)
                    print at_num.group()
