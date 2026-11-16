import os

from winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE

def returnDir() -> str | None:
    """
    Returns the recycle bin dir.
    
    :return: The name of the recycle bin dir as string or None
    :rtype: str|None
    """
    possibleDirs: list[str] = [
        "C:\\Recycler\\",
        "C:\\Recycled\\",
        "C:\\$Recycle.Bin\\"
    ]
    
    for recycleDir in possibleDirs:
        if os.path.isdir(recycleDir):
            return recycleDir
    return None

def translateSidtoUser(sid: str) -> str:
    """
    Translates SID to Username
    
    :param sid: The SID enumerated from Recycle bin
    :type sid: str
    
    :return: The username or the SID
    :rtype: str
    """
    try:
        key = OpenKey(
            HKEY_LOCAL_MACHINE,
            "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList" + "\\" + sid
        )
        (value, typeId) = QueryValueEx(key, "ProfileImagePath")
        user: str = value.split("\\")[-1]
        return user
    except:
        return sid

def findRecycled(recycleDir: str) -> None:
    """
    Opens the recycle directory and prints listed files
    
    :param recycleDir: The identified recycle bin
    :type recycleDir: str
    """
    dirList: list[str] = os.listdir(recycleDir)
    for sid in dirList:
        files: list[str] = os.listdir(recycleDir + sid)
        user: str = translateSidtoUser(sid)
        print(f"\n[*] Listing Files for User: {user}")
        
        for file in files:
            print(f"[+] Found file: {file}")

def main() -> None:
    recycleDir = returnDir()
    findRecycled(recycleDir=recycleDir)

if __name__ == "__main__":
    main()