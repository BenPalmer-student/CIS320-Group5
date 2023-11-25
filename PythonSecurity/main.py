import threading
import sys
import select
from packet_sniffer import PacketSniffer
from scp_transfer import SCPUploader  # Import the SCPUploader class

def listen_for_q(packet_sniffer):
    print("Press 'q' to quit.")
    while True:
        if select.select([sys.stdin], [], [], 0.1)[0]:
            key = sys.stdin.read(1)
            if key == 'q':
                packet_sniffer.stop()
                break

def main():
    packet_sniffer = PacketSniffer()
    listener_thread = threading.Thread(target=packet_sniffer.run)
    listener_thread.start()

    try:
        listen_for_q(packet_sniffer)
    except KeyboardInterrupt:
        pass
    finally:
        listener_thread.join()

    # Once the packet sniffer is stopped, initiate SCP file transfer
    scp_uploader = SCPUploader()
    scp_uploader.upload_file('packets.pcap')

if __name__ == '__main__':
    main()
