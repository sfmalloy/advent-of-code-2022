from io import TextIOWrapper

def start_point(packet: str, length: int) -> int:
    for i in range(len(packet)):
        if len(set(packet[i:i+length])) == length:
            return i+length
    return -1

def main(file: TextIOWrapper):
    packet = file.readline().strip()
    print(start_point(packet, 4))
    print(start_point(packet, 14))
