import socket
from random import choice
from sys import path
path.append("..")
import packet_builder
from time import sleep

request_lines = [
    'GET%00 / HTTP/1.1\r\n\r\n',
    'GET\0 / HTTP/1.1\r\n\r\n',
    'GET\t/\tHTTP/1.1\r\n\r\n',
    'GET / HTTP/1.1\r\n\r\n',
    'GET /// HTTP/1.1\r\n\r\n',
    'GET /../ HTTP/1.1\r\n\r\n',
    'GET /./ HTTP/1.1\r\n\r\n',
    'GET %2F HTTP/1.1\r\n\r\n',
    'GET %2F%2F%2F HTTP/1.1\r\n\r\n',
    'GET %2F%2E%2E%2F HTTP/1.1\r\n\r\n',
    'GET %2F%2E%2F HTTP/1.1\r\n\r\n',
    'GET\t%2F\tHTTP/1.1\r\n\r\n',
    'GET\t%2F%2F%2F\tHTTP/1.1\r\n\r\n',
    'GET\t%2F%2E%2E%2F\tHTTP/1.1\r\n\r\n',
    'GET\t%2F%2E%2F\tHTTP/1.1\r\n\r\n',
    'GET %2F..%2F HTTP/1.1\r\n\r\n',
    'GET /%2E%2E/ HTTP/1.1\r\n\r\n',
    'GET %2F.%2F HTTP/1.1\r\n\r\n',
    'GET /%2E/ HTTP/1.1\r\n\r\n',
]

def send_get_packet(destination_ip, destination_port):
    """Make TCP handshake by manually creating and sending SYN, SYN-ACK and ACK packets.
    
    Arguments:
    destination_ip -- the IP address of the target
    destination_port -- the targets port to which the packet will be sent 
    request_line -- the request line of HTTP GET method (payload)

    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                 
    s.connect((destination_ip, destination_port))
    print(".")
    s.send(choice(request_lines).encode("utf-8"))
    print("Send 1 packets")
    s.close()
    sleep(packet_builder.generate_delay())