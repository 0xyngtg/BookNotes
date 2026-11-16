import optparse
from ipaddress import ip_address
from scapy.all import sniff, sr1, conf
from scapy.layers.inet import IP, ICMP

ttlValues = {}
THRESH = 5


def is_private(ipsrc: str) -> bool:
    try:
        ip = ip_address(ipsrc)
    except ValueError:
        return False
    return ip.is_private or ip.is_loopback or ip.is_link_local


def checkTTL(ipsrc: str, ttl: str) -> None:
    if is_private(ipsrc):
        return
    if ipsrc not in ttlValues:
        pkt = sr1(IP(dst=ipsrc) / ICMP(), retry=0, timeout=1, verbose=0)
        if pkt is None or IP not in pkt:
            return 
        ttlValues[ipsrc] = pkt[IP].ttl
    if abs(int(ttl) - int(ttlValues[ipsrc])) > THRESH:
        print(f"\n[!] Detected Possible Spoofed Packet From: {ipsrc}")
        print(f"[!] TTL: {ttl}, Actual TTL: {ttlValues[ipsrc]}")


def testTTL(pkt) -> None:
    if IP not in pkt:
        return
    try:
        ipsrc = pkt[IP].src
        ttl = str(pkt[IP].ttl)
        checkTTL(ipsrc, ttl)
    except (AttributeError, ValueError):
        pass

def main():
    global THRESH
    parser = optparse.OptionParser("usage%prog -i<interface> -t <thresh>")
    parser.add_option('-i', dest='iface', type='string', help='network interface')
    parser.add_option('-t', dest='thresh', type='int', help='threshold count')
    (options, _) = parser.parse_args()

    if options.iface is not None:
        conf.iface = options.iface
    if options.thresh is not None:
        THRESH = options.thresh

    sniff(prn=testTTL, store=0)


if __name__ == '__main__':
    main()