import thinkgear

PORT = '/dev/rfcomm1'
for packets in thinkgear.ThinkGearProtocol(PORT).get_packets():
    for p in packets:
        if isinstance(p, thinkgear.ThinkGearRawWaveData):
            continue
        print p