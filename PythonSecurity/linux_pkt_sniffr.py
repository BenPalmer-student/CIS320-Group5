import socket
from pkt_capture import PCAPFile
from nettypes import EthernetFrame, IPHeader, TCPSegment, UDPSegment

#needs elevated privlages to work
def main():
    #setting up socket to bring in raw packet data
    #socket.AF_PACKET is ONLY available on linux
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    pcap = PCAPFile('packets.pcap')

    #infiniate loop used for polling the socket to grab as many packets as needed
    while True:
        #65535 is the max size that recvfrom can take
        #.recvfrom() returns a tuple where the first element is the raw data read from the socket and the second element is the address of the sender
        raw_data, addr = sock.recvfrom(65535)

        #for unpacking packet to stdout
        ethframe = EthernetFrame(raw_data)
        print(ethframe)
        if ethframe.protocol == 8:
            ipheader = IPHeader(ethframe.leftover_data)
            print(ipheader)
            #logic to check if tcp or udp
            if ipheader.protocol == 6:
                tcp = TCPSegment(ipheader.leftover_data)
                print(tcp)
            elif ipheader.protocol == 17:
                udp = UDPSegment(ipheader.leftover_data)
                print(udp)

        #for writing to pcap file for later analysis
        #pcap.write(raw_data)
    pcap.close()


if __name__ == '__main__':
    main()