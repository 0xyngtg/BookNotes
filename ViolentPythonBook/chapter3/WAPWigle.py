import os
import argparse
import urllib
import re

import mechanize
from winreg import HKEYType, OpenKey, EnumKey, EnumValue, CloseKey, HKEY_LOCAL_MACHINE

def val12Address(value: str) -> str:
    address = ""
    for ch in value:
        address += ("%02x "% ord(ch))
    address = address.strip(" ").replace(" ", ":")[0:17]
    return address

def wiglePrint(username: str, password: str, netID: str) -> None:
    browser: mechanize.Browser = mechanize.Browser()
    browser.open("https://wigle.net")
    
    data: dict[str, str] = {"credential_0": username, "credential_1": password}
    browser.open("https://wigle.net/gps/gps/main/login", data)
    
    params: dict[str, str] = {}
    params["netid"] = netID
    respURL: str = "https://wigle.net/gps/gps/main/confirmquery/"
    resp: bytes = browser.open(respURL, params).read()
    
    mapLat: str = "N/A"
    mapLon: str = "N/A"
    rLat: list[str]= re.findall(r"maplat=.*\&", resp)
    if rLat:
        mapLat = rLat[0].split("&")[0].split("=")[1]
    rLon: list[str] = re.findall(r"maplon=.*\&", resp)
    if rLon:
        mapLon = rLon[0].split()
    print(f"[-] Lat: {mapLat}, Lon: {mapLon}")

def printNetworks(username: str, password: str) -> None:
    network: str = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion" + "\\NetworkList\\Signatures\\Unmanaged"
    key: HKEYType = OpenKey(HKEY_LOCAL_MACHINE, network)
    print("\n[*] Networks joined:")
    for i in range(100):
        try:
            guid: str = EnumKey(key, i)
            networkKey = OpenKey(key, str(guid))
            (n, address, t) = EnumValue(networkKey, 5)
            (n, name, t) = EnumValue(networkKey, 4)
            macAddress = val12Address(address)
            networkName = str(name)
            print(f"[+] {networkName} {macAddress}")
            wiglePrint(username=username, password=password, netID=macAddress)
            CloseKey(networkKey)
        except:
            break

def arguments() -> argparse.Namespace:
    args: argparse.ArgumentParser = argparse.ArgumentParser()
    args.add_argument("-u", dest="username", type="string", help="Specify Wigle username")
    args.add_argument("-p", dest="password", type="string", help="Specify Wigle password")
    return args.parse_args()

def main() -> None:
    args = arguments()
    username: str = args.username
    password: str = args.password
    
    if username == None or password == None:
        exit(0)
    else:
        printNetworks(username=username, password=password)

if __name__ == "__main__":
    main()
