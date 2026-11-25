from scapy.all import *
from scapy.layers.inet import IP, UDP, ICMP

def ddosTest(source: str, destination: str, interface: str, count: int) -> None:
    pkt: Packet = IP(src=source, dst=destination)/ICMP(type=8, id=678)/Raw(load="1234")
    send(pkt, iface=interface, count=count)
    
    pkt = IP(src=source, dst=destination)/ICMP(type=8)/Raw(load="AAAAAAAAA")
    send(pkt, iface=interface, count=count)
    
    pkt = IP(src=source, dst=destination)/UDP(dport=31335)/Raw(load="PONG")
    send(pkt, iface=interface, count=count)
    
    pkt = IP(src=source, dst=destination)/ICMP(type=0, id=456)
    send(pkt, iface=interface, count=count)

def exploitTest(source: str, destination: str, interface: str, count: int) -> None:
    payload: str = "\x01\x03\x00\x00\x00\x00\x00\x01\x00\x02\x02\xE8"
    pkt: Packet = IP(src=source, dst=destination)/UDP(dport=518)/Raw(load=payload)
    send(pkt, iface=interface, count=count)
    
    payload = "^\xB0\x02\x89\x06\xFE\xC8\x89F\x04\xB0\x06\x89F"
    pkt = IP(src=source, dst=destination)/UDP(dport=635)/Raw(load=payload)
    send(pkt, iface=interface, count=count)

def scanTest(source: str, destination: str, interface: str, count: int) -> None:
    pkt: Packet = IP(src=source, dst=destination)/UDP(dport=7)/Raw(load="cybercop")
    send(pkt)
    
    pkt = IP(src=source, dst=destination)/UDP(dport=10080)/Raw(load="Amanda")
    send(pkt, iface=interface, count=count)

def main() -> None:
    source: str = "1.3.3.7"
    destination: str = "192.168.1.106"
    interface: str = "eth0"
    count: int = 1
    
    ddosTest(
        source=source,
        destination=destination,
        interface=interface,
        count=count
    )
    
    exploitTest(
        source=source,
        destination=destination,
        interface=interface,
        count=count
    )

if __name__ == "__main__":
    main()


# TARGET SNORT RULES:
#     ddosTest
#         /etc/snort/rules/ddos.rules <..SNIPPED..> alert icmp $EXTERNAL_NET any -> $HOME_NET any (msg:"DDOS TFN Probe"; icmp_id:678; itype:8; content:"1234"; reference:arachnids,443; classtype:attempted-recon; sid:221; rev:4;) alert icmp $EXTERNAL_NET any -> $HOME_NET any (msg:"DDOS tfn2k icmp possible communication"; icmp_id:0; itype:0; content:"AAAAAAAAAA"; reference:arachnids,425; classtype:attempted-dos; sid:222; rev:2;) alert udp $EXTERNAL_NET any -> $HOME_NET 31335 (msg:"DDOS Trin00 Daemon to Master PONG message detected"; content:"PONG"; reference:arachnids,187; classtype:attempted-recon; sid:223; rev:3;) alert icmp $EXTERNAL_NET any -> $HOME_NET any (msg:"DDOS TFN client command BE"; icmp_id:456; icmp_seq:0; itype:0; reference:arachnids,184; classtype:attempted-dos; sid:228; rev:3;) <...SNIPPED...>
#     exploitTest
#         /etc/snort/rules/exploit.rules => ntalkd x86 Linux overflow and Linux mountd overflow
#     scanTest
#         reconnaissance rules

# LOGS EXAMPLE:
#     victim# snort -q -A console -i eth0 -c /etc/snort/snort.conf 03/14-11:45:01.060632 [**] [1:222:2] DDOS tfn2k icmp possible communication [**] [Classification: Attempted Denial of Service] [Priority: 2] {ICMP} 1.3.3.7 -> 192.168.1.106 03/14-11:45:01.066621 [**] [1:223:3] DDOS Trin00 Daemon to Master PONG message detected [**] [Classification: Attempted Information Leak] [Priority: 2] {UDP} 1.3.3.7:53 -> 192.168.1.106:31335 03/14-11:45:01.069044 [**] [1:228:3] DDOS TFN client command BE [**] [Classification: Attempted Denial of Service] [Priority: 2] {ICMP} 1.3.3.7 -> 192.168.1.106 03/14-11:45:01.071205 [**] [1:313:4] EXPLOIT ntalkd x86 Linux overflow [**] [Classification: Attempted Administrator Privilege Gain] [Priority: 1] {UDP} 1.3.3.7:53 -> 192.168.1.106:518 03/14-11:45:01.076879 [**] [1:315:6] EXPLOIT x86 Linux mountd overflow [**] [Classification: Attempted Administrator Privilege Gain] [Priority: 1] {UDP} 1.3.3.7:53 -> 192.168.1.106:635 03/14-11:45:01.079864 [**] [1:636:1] SCAN cybercop udp bomb [**] [Classification: Potentially Bad Traffic] [Priority: 2] {UDP} 1.3.3.7:53 -> 192.168.1.106:7 03/14-11:45:01.082434 [**] [1:634:2] SCAN Amanda client version request [**] [Classification: Attempted Information Leak] [Priority: 2] {UDP} 1.3.3.7:53 -> 192.168.1.106:10080
