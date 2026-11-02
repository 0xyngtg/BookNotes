###
# "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\Current Version\NetworkList\Signatures\Unmanaged"
# ProfileGuid (REG_SZ)
# Description (REG_SZ)
# Source (REG_DWORD)
# DnsSuffix (REG_SZ)
# FirstNetwork (REG_SZ)
# DefaultGatewayMac (REG_BINARY) => Hex bytes that refer to the actual MAC address
###
from winreg import HKEYType, OpenKey, EnumKey, EnumValue, CloseKey, HKEY_LOCAL_MACHINE

def val12Address(value: str) -> str:
    address = ""
    for ch in value:
        address += ("%02x "% ord(ch))
    address = address.strip(" ").replace(" ", ":")[0:17]
    return address

def printNetworks() -> None:
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
            CloseKey(networkKey)
        except:
            break

def main() -> None:
    printNetworks()

if __name__ == "__main__":
    main()
