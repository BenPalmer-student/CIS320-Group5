import socket
from struct import unpack
from utils import mac_addr

class EthernetFrame:
    #grabbing the first 14 characters of the packet
    length = 14
    def __init__(self, data):
        #unpack data using format strings using functions from struct module
        #"!" indicates network big-endian, "6s" indicates a char array of size 6, and "h" is an unsigned int indicating protocol used in packet
        unpacked_data = unpack('!6s6sh', data[0:self.length])
        #.ntoh() is a conversion function from socket module 
        self.protocol = socket.ntoh(unpacked_data[2])
        self.destination = mac_addr(data[0:6])
        self.source = mac_addr(data[6:12])
        self.leftover_data = data[self.length:]

    #tostring function to make output all pretty
    def __str__(self):
        return """
            ______________________________
            ------------------------------
            Ethernet Frame...
                Source:         {source}
                Destination:    {destination}
                Protocol:       {protocol}
            """.format(**self.__dict__)
    
class IPHeader:
    #ip header is first 20 bytes of "leftover data" after pulling the Ethernet Frame off 
    length = 20
    def __init__(self, data):
        unpacked_data = unpack('!BBHHBBH4s4s', data[0:self.length])
        #>> is python binary right shift
        self.version = data[0] >> 4
        self.header_length = (data[0] & 15) * 4
        self.ttl = unpacked_data[5]
        self.protocol = unpacked_data[6]
        self.source_addr = socket.inet_ntoa(unpacked_data[8])
        self.dest_addr = socket.inet_ntoa(unpacked_data[9])
        self.leftover_data = data[self.length:]
    
    #tostring function to make output pretty
    def __str__(self):
        return """
            IP Header...
                Source Address:         {source_addr}
                Destination Address:    {dest_addr}
                Protocol:               {protocol}
            """.format(**self.__dict__)

class TCPSegment:
    #TCP segment is 20 bytes
    length = 20
    def __init__(self, data):
        unpacked_data = unpack('!HHLLBBHHH', data[0:self.length])
        self.src_port = unpacked_data[0]
        self.dest_port = unpacked_data[1]
        self.sequence = unpacked_data[2]
        self.acknowlegement = unpacked_data[3]
        self.offset_reserved = unpacked_data[4]
        self.header_length = self.offset_reserved >> 4
        self.leftover_data = self.parse_data_http(data[self.length:])

    #tostring function
    def __str__(self):
        return """
            TCP Segment...
            Source Port:        {src_port}
            Destination Port:   {dest_port}
            Data:               {leftover_data}
        """.format(**self.__dict__)
    
    #func to parse http headers if they exist in leftover_data
    def parse_data_http(self, data):
        try:
            return data.decode('utf-8')
        except Exception as e:
            return data
        
class UDPSegment:
    length = 8
    def __init__(self, data):
        unpacked_data = unpack('!HHHH', data[0:self.length])
        self.src_port = unpacked_data[0]
        self.dest_port = unpacked_data[1]
        self.length = unpacked_data[2]
        self.checksum = unpacked_data[3]
        self.leftover_data = data[self.length:]

    def __str__(self):
        return """
            UDP Segment...
            Source Port:        {src_port}
            Destination Port:   {dest_port}
            Checksum:           {checksum}
            Data:               {leftover_data}
        """.format(**self.__dict__)
