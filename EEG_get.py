import thinkgear

PORT = '/dev/rfcomm1'

def check_method(terget):
    print type(terget)
    for x in dir(terget):
        print x

if __name__ == "__main__":
# check_method(thinkgear)

# for packets in thinkgear.ThinkGearProtocol(PORT).get_packets():
#     for p in packets:
#         if isinstance(p, thinkgear.ThinkGearRawWaveData):
#             continue
#         print p
