from scapy.all import RandShort, send, IP, TCP, sr1
from random import choice
from sys import path
path.append("..")
import packet_builder

request_lines = [
    'GET%00 / HTTP/1.1\r\n',
    'GET\0 / HTTP/1.1\r\n',
    'GET\t/\tHTTP/1.1\r\n',
    'GET / HTTP/1.1\r\n',
    'GET /// HTTP/1.1\r\n',
    'GET /../ HTTP/1.1\r\n',
    'GET /./ HTTP/1.1\r\n',
    'GET %2F HTTP/1.1\r\n',
    'GET %2F%2F%2F HTTP/1.1\r\n',
    'GET %2F%2E%2E%2F HTTP/1.1\r\n',
    'GET %2F%2E%2F HTTP/1.1\r\n',
    'GET\t%2F\tHTTP/1.1\r\n',
    'GET\t%2F%2F%2F\tHTTP/1.1\r\n',
    'GET\t%2F%2E%2E%2F\tHTTP/1.1\r\n',
    'GET\t%2F%2E%2F\tHTTP/1.1\r\n',
    'GET %2F..%2F HTTP/1.1\r\n',
    'GET /%2E%2E/ HTTP/1.1\r\n',
    'GET %2F.%2F HTTP/1.1\r\n',
    'GET /%2E/ HTTP/1.1\r\n',
]

def make_tcp_handshake(destination_ip, request_line):
    """Make TCP handshake by manually creating and sending SYN, SYN-ACK and ACK packets.
    
    Argument:
    destination_ip -- the IP address of the target
    request_line -- the request line of HTTP GET method in TCP handshake stage

    """
    syn=IP(dst=destination_ip)/TCP(sport=RandShort(), dport=80, flags="S")
    syn_ack=sr1(syn)

    #ack packet
    return IP(dst=destination_ip)/TCP(sport=syn_ack.dport, dport=80, flags="A", seq=syn_ack.ack, ack=syn_ack.seq + 1) / request_line 

def send_get_packet(destination_ip):
    """Send HTTP GET request"""
    send(make_tcp_handshake(destination_ip, choice(request_lines)), inter=packet_builder.generate_delay())