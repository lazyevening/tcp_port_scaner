import argparse
import socket
import threading
import time


def UDP_connect(ip, port_number, delay):
    pass


def TCP_connect(ip, port_number, delay):
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.settimeout(delay)
    try:
        tcp_sock.connect((ip, port_number))
        print(port_number)
    except socket.error:
        pass


def scan_ports(host_ip, delay, from_port, to_port):
    if to_port > 65535:
        raise AttributeError("end port have to be less then 65536")
    thread_count = 256

    if to_port < thread_count:
        thread_count = to_port
    target = TCP_connect
    for _ in range(2):
        port = from_port
        while port <= to_port:
            threads = []
            for i in range(thread_count):

                if port + i > to_port:
                    break
                t = threading.Thread(target=target, args=(host_ip, i + port, delay))
                threads.append(t)
            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()
            port += thread_count
        target = UDP_connect


def main():
    start = time.time()
    parser = argparse.ArgumentParser(description="Ping script")
    parser.add_argument("host", help="IP or name to ping")
    parser.add_argument("interval", help="From port to port")

    args = parser.parse_args()
    delay = 1
    scan_ports(args.host, delay, int(args.interval.split('-')[0]), int(args.interval.split('-')[1]))
    print(time.time() - start)


if __name__ == "__main__":
    main()
