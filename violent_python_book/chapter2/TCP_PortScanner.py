import argparse
import socket
from threading import Thread, Semaphore

screenLock = Semaphore(value=1)

def getArguments() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="TCP Port Scanner",
        )
    parser.add_argument(
        "-H", "--host",
        type=str,
        required=True,
        help="Specify target host"
        )
    parser.add_argument(
        "-p", "--port",
        type=str,
        required=False,
        help="Specify target port[s] separated by comma (-p 80,443)"
        )
    return parser.parse_args()

def connectPort(targetHost: str, targetPort: int) -> None:
    try:
        connSocket: socket.socket = socket.socket(
            socket.AF_INET, 
            socket.SOCK_STREAM
            )
        connSocket.connect((targetHost, targetPort))
        connSocket.send(b'ViolentPython\r\n')
        results: bytes = connSocket.recv(100)
        screenLock.acquire()
        print(f"[+] TCP Port open: {targetPort}\n{results.decode(errors="replace")}")
    except:
        screenLock.acquire()
        print(f"[-] TCP Closed")
    finally:
        screenLock.release()
        connSocket.close()

def resolveHostIP(targetHost: str) -> str|None:
    try:
        targetIP: str = socket.gethostbyname(targetHost)
        return targetIP
    except:
        print(f"[-] Can not resolve {targetHost}: Unknown host")
        return

def resolveHostName(targetIP: str) -> None:
    try:
        targetName: tuple[str, list[str], list[str]] = socket.gethostbyaddr(targetIP)
        print(f"[+] Scan Results for: {targetName[0]}")
    except:
        print(f"[+] Scan Results for: {targetIP}")

def scanPort(targetHost: str, targetPorts:list[str]) -> None:
    targetIP: str|None = resolveHostIP(targetHost=targetHost)
    if not targetIP:
        return
    resolveHostName(targetIP=targetIP)
    socket.setdefaulttimeout(1)
    for targetPort in targetPorts:
        print(f"[*] Scanning port {targetPort}")
        t = Thread(target=connectPort, args=(targetHost, int(targetPort)))
        t.start()

def main() -> None:
    args: argparse.Namespace = getArguments()
    if args.port:
        scanPort(targetHost=args.host, targetPorts=list(args.port.split(',')))
    else:
        scanPort(targetHost=args.host, targetPorts=list(str(range(65535))))

if __name__ == "__main__":
    main()
