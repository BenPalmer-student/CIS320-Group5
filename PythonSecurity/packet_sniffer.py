import socket
from pkt_capture import PCAPFile
from nettypes import EthernetFrame, IPHeader, TCPSegment, UDPSegment

class PacketSniffer:
    def __init__(self):
        # Set up the raw socket and PCAP file
        self.sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        self.pcap = PCAPFile('packets.pcap')
        self.running = True

    def run(self):
        while self.running:
            # Receive raw packet data
            raw_data, addr = self.sock.recvfrom(65535)

            # Process the packet data
            ethframe = EthernetFrame(raw_data)
            print(ethframe)
            if ethframe.protocol == 8:
                ipheader = IPHeader(ethframe.leftover_data)
                print(ipheader)
                if ipheader.protocol == 6:
                    tcp = TCPSegment(ipheader.leftover_data)
                    print(tcp)
                elif ipheader.protocol == 17:
                    udp = UDPSegment(ipheader.leftover_data)
                    print(udp)

            # Write the packet data to the PCAP file
            self.pcap.write(raw_data)

        # Close the PCAP file when the packet sniffer stops
        self.pcap.close()

    def stop(self):
        # Set running to False to stop the packet sniffer
        self.running = False
