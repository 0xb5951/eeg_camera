import re
import thinkgear

PORT = '/dev/rfcomm1'

def check_method(terget):
    print type(terget)
    for x in dir(terget):
        print x

if __name__ == "__main__":
    # check_method(thinkgear)
    for packets in thinkgear.ThinkGearProtocol(PORT).get_packets():
        for pkt in packets:
            if isinstance(pkt, thinkgear.ThinkGearRawWaveData):
                continue

            t = str(pkt)
            # print t

            if t != '':
                if "ATTENTION" in t:
                    at_num = re.search(r'\d+', t)
                    print at_num.group()
