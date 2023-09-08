from struct import pack
import time

class PCAPFile:
    def __init__(self, filename):
        #wb tag sets write mode, specifically for binary strings
        self.fp = open(filename, 'wb')
        #PACP files have a specific header that is necessary, this line just creates the header so programs like WireShark/TCPDump see this file as a valid PCAP
        header = pack('!IHHiIII', 0xa1b2c3d4, 2, 4, 0, 0, 65535, 1)
        self.fp.write(header)
    
    def write(self, data):
        #generating timestamps for each packet, seconds/microseconds
        seconds, mseconds = [int(part) for part in str(time.time()).split('.')]
        length = len(data)
        message = pack('!IIII', seconds, mseconds, length, length)
        self.fp.write(message)
        self.fp.write(data)

    def close(self):
        self.fp.close()